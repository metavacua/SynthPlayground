"""
An orchestrator for executing Unrestricted Development Cycle (UDC) plans.

This script provides a sandboxed environment for running UDC plans, which are
low-level assembly-like programs that can perform Turing-complete computations.
The orchestrator acts as a virtual machine with a tape-based memory model,
registers, and a set of simple instructions.

To prevent non-termination and other resource-exhaustion issues, the
orchestrator imposes strict limits on the number of instructions executed,
the amount of memory used, and the total wall-clock time.
"""

import argparse
import re
import time
from collections import defaultdict
from typing import Dict, List, Any


# A simple representation of a parsed instruction
class Instruction:
    def __init__(self, opcode: str, args: List[str]):
        self.opcode = opcode
        self.args = args

    def __repr__(self):
        return f"Instruction(opcode='{self.opcode}', args={self.args})"


class UDCOrchestrator:
    """
    Executes an Unrestricted Development Cycle (UDC) plan within a sandboxed
    Turing Machine-like environment with strict resource limits.
    """

    def __init__(
        self,
        plan_path: str,
        max_instructions: int = 10000,
        max_memory_cells: int = 1000,
        max_time_s: int = 5,
    ):
        self.plan_path = plan_path
        self.max_instructions = max_instructions
        self.max_memory_cells = max_memory_cells
        self.max_time_s = max_time_s

        # VM State
        self.instructions: List[Instruction] = []
        self.labels: Dict[str, int] = {}
        self.tape: Dict[int, Any] = defaultdict(int)
        self.head_pos: int = 0
        self.registers: Dict[str, int] = defaultdict(int)
        self.ip: int = 0  # Instruction Pointer

        # Comparison flags
        self.cmp_flag_equal: bool = False
        self.cmp_flag_greater: bool = False

        # Execution control
        self.running: bool = False
        self.instruction_count: int = 0
        self.start_time: float = 0.0

    def run(self):
        """
        Parses and runs the UDC plan until it halts or a limit is exceeded.
        """
        print("--- UDC Orchestrator Initializing ---")
        print(f"Plan: {self.plan_path}")
        print(
            f"Limits: {self.max_instructions} instructions, {self.max_memory_cells} memory cells, {self.max_time_s}s wall-clock time."
        )

        self._parse_plan()

        self.running = True
        self.start_time = time.time()

        print("\n--- Execution Started ---")
        while self.running:
            # 1. Check all safety limits before executing the next instruction
            if self.instruction_count >= self.max_instructions:
                print(
                    f"\nERROR: Exceeded maximum instruction limit ({self.max_instructions}). Terminating."
                )
                break
            if time.time() - self.start_time >= self.max_time_s:
                print(
                    f"\nERROR: Exceeded maximum wall-clock time ({self.max_time_s}s). Terminating."
                )
                break
            if len(self.tape) > self.max_memory_cells:
                print(
                    f"\nERROR: Exceeded maximum memory cells ({self.max_memory_cells}). Terminating."
                )
                break

            # 2. Fetch and execute
            if self.ip >= len(self.instructions):
                print("\nWARNING: Reached end of plan without HALT instruction.")
                break

            instruction = self.instructions[self.ip]

            # Store old IP to detect jumps
            old_ip = self.ip
            self._execute_instruction(instruction)

            # Increment IP only if it wasn't changed by a jump instruction
            if self.ip == old_ip:
                self.ip += 1

            self.instruction_count += 1

        print("\n--- Execution Finished ---")
        print(f"Total instructions executed: {self.instruction_count}")
        print(f"Final head position: {self.head_pos}")
        print("Final non-zero tape contents:")
        for pos, val in sorted(self.tape.items()):
            if val != 0:
                print(f"  Tape[{pos}] = {val}")

    def _parse_plan(self):
        with open(self.plan_path, "r") as f:
            lines = f.readlines()
            for line_content in lines:
                line_stripped = line_content.strip()
                if not line_stripped or line_stripped.startswith("#"):
                    continue

                line_stripped = line_stripped.split("#", 1)[0].strip()
                parts = re.split(r"\s+", line_stripped)
                opcode = parts[0].upper()
                args = parts[1:]

                if opcode == "LABEL":
                    if len(args) == 1:
                        self.labels[args[0]] = len(self.instructions)
                else:
                    self.instructions.append(Instruction(opcode, args))

    def _get_value(self, arg: str) -> int:
        """Resolves an argument to an integer value, either from a register or a literal."""
        # If the argument can be parsed as an integer, treat it as a literal.
        try:
            return int(arg)
        except ValueError:
            # Otherwise, treat it as a register. The defaultdict will return 0 if it's new.
            return self.registers[arg.upper()]

    def _execute_instruction(self, instruction: Instruction):
        opcode = instruction.opcode
        args = instruction.args

        # Tape Operations
        if opcode == "LEFT":
            self.head_pos -= 1
        elif opcode == "RIGHT":
            self.head_pos += 1
        elif opcode == "READ":
            self.registers[args[0].upper()] = self.tape[self.head_pos]
        elif opcode == "WRITE":
            self.tape[self.head_pos] = self._get_value(args[0])

        # Data Movement
        elif opcode == "MOV":
            self.registers[args[0].upper()] = self._get_value(args[1])

        # Arithmetic
        elif opcode == "ADD":
            self.registers[args[0].upper()] += self._get_value(args[1])
        elif opcode == "SUB":
            self.registers[args[0].upper()] -= self._get_value(args[1])
        elif opcode == "INC":
            self.registers[args[0].upper()] += 1
        elif opcode == "DEC":
            self.registers[args[0].upper()] -= 1

        # Control Flow
        elif opcode == "JMP":
            self.ip = self.labels[args[0]]
        elif opcode == "CMP":
            val1 = self._get_value(args[0])
            val2 = self._get_value(args[1])
            self.cmp_flag_equal = val1 == val2
            self.cmp_flag_greater = val1 > val2
        elif opcode == "JE" and self.cmp_flag_equal:
            self.ip = self.labels[args[0]]
        elif opcode == "JNE" and not self.cmp_flag_equal:
            self.ip = self.labels[args[0]]
        elif opcode == "JG" and self.cmp_flag_greater:
            self.ip = self.labels[args[0]]
        elif opcode == "JL" and not self.cmp_flag_greater and not self.cmp_flag_equal:
            self.ip = self.labels[args[0]]

        # Execution
        elif opcode == "HALT":
            print("\nHALT instruction encountered. Execution successful.")
            self.running = False
        elif opcode == "CALL":
            print(
                f"SANDBOXED TOOL CALL: {args[0]} with args {args[1:]} (Not implemented)"
            )
            # In a real implementation, this would call a secure, sandboxed tool runner.

        else:
            # For Jumps that don't meet their condition, we do nothing and let IP increment.
            pass


def main():
    parser = argparse.ArgumentParser(
        description="Executes a UDC plan with strict resource limits."
    )
    parser.add_argument("plan_path", help="The path to the .udc plan file.")
    parser.add_argument(
        "--max-instructions",
        type=int,
        default=10000,
        help="Max instructions to execute.",
    )
    parser.add_argument(
        "--max-memory", type=int, default=1000, help="Max memory cells to use."
    )
    parser.add_argument(
        "--max-time", type=int, default=5, help="Max wall-clock time in seconds."
    )
    args = parser.parse_args()

    orchestrator = UDCOrchestrator(
        plan_path=args.plan_path,
        max_instructions=args.max_instructions,
        max_memory_cells=args.max_memory,
        max_time_s=args.max_time,
    )
    orchestrator.run()


if __name__ == "__main__":
    main()
