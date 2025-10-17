import argparse
import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# A simple representation of a parsed instruction
@dataclass
class Instruction:
    line_number: int
    original_line: str
    opcode: str
    args: List[str]

# A representation of a detected loop
@dataclass
class Loop:
    start_line: int
    end_line: int
    exit_condition: Optional[Instruction]
    risk: str = "UNKNOWN"
    reason: str = "Analysis has not been performed."

class HaltingHeuristicAnalyzer:
    """
    Performs static analysis on a UDC plan to provide a heuristic-based
    estimate of its likelihood to terminate.
    """

    def __init__(self, plan_path: str):
        self.plan_path = plan_path
        self.instructions: List[Instruction] = []
        self.labels: Dict[str, int] = {} # Maps label name to instruction index

    def analyze(self) -> Dict:
        """
        Runs the full analysis pipeline and returns a report.
        """
        try:
            self._parse_plan()
            loops = self._detect_loops()
            analyzed_loops = [self._analyze_loop(loop) for loop in loops]

            # Determine overall risk based on the highest risk loop
            overall_risk = "LOW"
            if not analyzed_loops:
                reason = "No loops detected. Termination risk is considered low."
            else:
                if any(l.risk == "HIGH" for l in analyzed_loops):
                    overall_risk = "HIGH"
                elif any(l.risk == "MEDIUM" for l in analyzed_loops):
                    overall_risk = "MEDIUM"
                elif any(l.risk == "UNKNOWN" for l in analyzed_loops):
                    overall_risk = "UNKNOWN"

                reason = f"Analysis complete. Found {len(analyzed_loops)} loop(s)."
                if overall_risk == "HIGH":
                    reason += " At least one loop has a high risk of not terminating."
                elif overall_risk == "MEDIUM":
                    reason += " At least one loop has a medium risk of not terminating."

            return self._generate_report(overall_risk, reason, analyzed_loops)

        except FileNotFoundError:
            return self._generate_report("ERROR", f"File not found: {self.plan_path}", [])
        except Exception as e:
            return self._generate_report("ERROR", f"An error occurred during analysis: {e}", [])

    def _parse_plan(self):
        """
        Parses the .udc file into instructions and builds a label map.
        Labels point to the index of the *next* instruction in the list.
        """
        instruction_index = 0
        with open(self.plan_path, 'r') as f:
            lines = f.readlines()
            for i, line_content in enumerate(lines):
                line_num = i + 1
                line_stripped = line_content.strip()

                if not line_stripped or line_stripped.startswith('#'):
                    continue

                line_stripped = line_stripped.split('#', 1)[0].strip()
                parts = re.split(r'\s+', line_stripped)
                opcode = parts[0].upper()
                args = parts[1:]

                if opcode == "LABEL":
                    if len(args) == 1:
                        self.labels[args[0]] = instruction_index
                    # Do not add LABEL as an instruction itself
                else:
                    self.instructions.append(Instruction(line_num, line_stripped, opcode, args))
                    instruction_index += 1

    def _detect_loops(self) -> List[Loop]:
        """
        Detects loops by finding backward jumps.
        """
        loops = []
        jump_opcodes = {"JMP", "JE", "JNE", "JG", "JL", "JGE", "JLE"}

        for idx, instruction in enumerate(self.instructions):
            if instruction.opcode in jump_opcodes:
                if not instruction.args:
                    continue

                label = instruction.args[0]
                if label in self.labels:
                    target_idx = self.labels[label]
                    # A backward jump is a sufficient condition for a loop
                    if target_idx < idx:
                        # The conditional jump is the primary exit condition
                        exit_cond = instruction if instruction.opcode != "JMP" else None
                        loops.append(Loop(
                            start_line=self.instructions[target_idx].line_number,
                            end_line=instruction.line_number,
                            exit_condition=exit_cond
                        ))
        return loops

    def _analyze_loop(self, loop: Loop) -> Loop:
        """
        Analyzes a single loop to determine its termination risk.
        This is the heuristic core of the analyzer.
        """
        if not loop.exit_condition:
            loop.risk = "HIGH"
            loop.reason = "Loop is unconditional (JMP) and has no detectable internal break."
            return loop

        # Find the CMP instruction associated with the exit condition
        exit_cond_instr = loop.exit_condition
        current_idx = self.instructions.index(exit_cond_instr)

        # Search backwards from the jump for the relevant CMP
        cmp_instr = None
        for i in range(current_idx - 1, -1, -1):
            if self.instructions[i].opcode == 'CMP':
                cmp_instr = self.instructions[i]
                break

        if not cmp_instr or len(cmp_instr.args) != 2:
            loop.risk = "MEDIUM"
            loop.reason = "Loop exit condition is not preceded by a clear 'CMP reg, val' instruction."
            return loop

        reg_to_check = cmp_instr.args[0]

        # Scan the body of the loop for modifications to this register
        loop_start_idx = self.labels.get(exit_cond_instr.args[0], -1)
        if loop_start_idx == -1: # Should not happen if loop was detected correctly
            loop.risk = "UNKNOWN"
            loop.reason = "Internal error: Could not find loop start label."
            return loop

        loop_body_instructions = self.instructions[loop_start_idx:current_idx]

        modifying_instructions = []
        is_dependent_on_read = False
        for instr in loop_body_instructions:
            # Check for modifications to the register we care about
            if instr.opcode in {"INC", "DEC"} and instr.args[0] == reg_to_check:
                modifying_instructions.append(instr)
            elif instr.opcode in {"ADD", "SUB", "MOV"} and instr.args[0] == reg_to_check:
                modifying_instructions.append(instr)

            # Check if the register's value comes from an unpredictable source
            if instr.opcode == "READ" and instr.args[0] == reg_to_check:
                is_dependent_on_read = True
                break

        if is_dependent_on_read:
            loop.risk = "HIGH"
            loop.reason = f"Loop exit depends on register '{reg_to_check}', which is modified by a 'READ' instruction inside the loop. Its value is unpredictable."
            return loop

        if not modifying_instructions:
            loop.risk = "HIGH"
            loop.reason = f"Loop exit depends on register '{reg_to_check}', but this register is not modified inside the loop body."
            return loop

        # Heuristic: if mods are complex (e.g., MOV from another register), risk is medium.
        # If mods are simple increments/decrements, risk is low.
        unpredictable_mods = [
            i for i in modifying_instructions
            if i.opcode in {"ADD", "SUB", "MOV"} and not i.args[1].lstrip('-').isdigit()
        ]

        if unpredictable_mods:
            loop.risk = "MEDIUM"
            loop.reason = f"Loop exit depends on register '{reg_to_check}', which is modified in a complex way (e.g., from another register '{unpredictable_mods[0].args[1]}')."
            return loop

        # If we only have predictable modifications, we can assume it's low risk.
        # A more advanced analyzer would check if the modification moves *towards* the exit value.
        loop.risk = "LOW"
        loop.reason = f"Loop exit depends on register '{reg_to_check}', which appears to be modified predictably (e.g., INC, DEC, or with literals)."
        return loop

    def _generate_report(self, risk: str, reason: str, loops: List[Loop]) -> Dict:
        """
        Formats the analysis results into a JSON-compatible dictionary.
        """
        # Convert dataclasses to dicts for JSON serialization
        loop_dicts = []
        for loop in loops:
            loop_dict = loop.__dict__
            if loop.exit_condition:
                loop_dict['exit_condition'] = loop.exit_condition.__dict__
            loop_dicts.append(loop_dict)

        return {
            "estimated_risk": risk,
            "reason": reason,
            "potential_infinite_loops": loop_dicts,
        }


def main():
    """
    Main entry point for the command-line tool.
    """
    parser = argparse.ArgumentParser(
        description="Analyzes a UDC plan for non-termination risk. Outputs a JSON report."
    )
    parser.add_argument(
        "plan_path", help="The path to the .udc plan file to analyze."
    )
    args = parser.parse_args()

    analyzer = HaltingHeuristicAnalyzer(args.plan_path)
    report = analyzer.analyze()

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()