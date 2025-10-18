"""
A paraconsistent execution model for UDC plans.

This module provides the classes necessary to interpret a UDC (Un-decidable
Computation) plan within a Logic of Formal Inconsistency (LFI). Instead of
concrete values, the state of the machine (registers, tape, etc.) is modeled
using paraconsistent truth values (TRUE, FALSE, BOTH, NEITHER).

This allows the system to reason about paradoxical programs, such as a program
that halts if and only if it does not halt. By executing the program under
paraconsistent semantics, the model can arrive at a final state of `BOTH`,
effectively demonstrating the paradoxical nature of the input without crashing.

Key classes:
- `ParaconsistentTruth`: An enum for the four truth values.
- `ParaconsistentState`: A wrapper for a value that holds a paraconsistent truth.
- `LFIInstruction`: A UDC instruction that operates on paraconsistent states.
- `LFIExecutor`: A virtual machine that executes a UDC plan using LFI semantics.
- `ParaconsistentHaltingDecider`: The main entry point that orchestrates the
  analysis of a UDC plan.
"""
import enum
import re
from tooling.halting_heuristic_analyzer import Instruction as UDCInstruction


class ParaconsistentTruth(enum.Enum):
    """
    Represents the four truth values in a first-degree entailment logic (FDE),
    which is a common foundation for Logics of Formal Inconsistency.
    """
    FALSE = {False}
    TRUE = {True}
    BOTH = {True, False}
    NEITHER = set()

    def __str__(self):
        return self.name

class ParaconsistentState:
    """
    A variable whose truth value is modeled paraconsistently.
    It can be true, false, both, or neither.
    """
    def __init__(self, value: ParaconsistentTruth = ParaconsistentTruth.NEITHER):
        self.value = value

    def is_true(self) -> bool:
        """Classical check: Is True in the value set?"""
        return True in self.value.value

    def is_false(self) -> bool:
        """Classical check: Is False in the value set?"""
        return False in self.value.value

    def is_consistent(self) -> bool:
        """A state is consistent if it's not BOTH."""
        return self.value != ParaconsistentTruth.BOTH

    def __repr__(self):
        return f"ParaconsistentState({self.value})"

class LFIInstruction:
    """A wrapper for UDC instructions to be used in the LFI Executor."""
    def __init__(self, opcode: str, args: list):
        self.opcode = opcode
        self.args = args

    def execute(self, executor: 'LFIExecutor'):
        """Executes the instruction on the given LFI executor state."""
        # This will be a large dispatch table, similar to the original orchestrator
        method_name = f"_exec_{self.opcode.lower()}"
        method = getattr(self, method_name, self._exec_unknown)
        method(executor)

    def _exec_unknown(self, executor: 'LFIExecutor'):
        # For now, we'll treat unknown instructions as no-ops.
        pass

    def _exec_halt(self, executor: 'LFIExecutor'):
        """The HALT instruction sets the halted state to TRUE."""
        # In LFI, we add truth values.
        # If it was FALSE, it becomes {True, False} -> BOTH
        # If it was NEITHER, it becomes {True} -> TRUE
        new_value = executor.halted.value.value | {True}
        executor.halted.value = ParaconsistentTruth(new_value)
        # We also stop this path of execution.
        executor.ip = len(executor.instructions)


    def __repr__(self):
        return f"LFIInstruction(opcode='{self.opcode}', args={self.args})"

    # --- Placeholder methods for other instructions ---
    # In a full implementation, these would manipulate paraconsistent states.
    # For this demonstration, we only need HALT to be fully modeled.
    def _exec_left(self, executor: 'LFIExecutor'): pass
    def _exec_right(self, executor: 'LFIExecutor'): pass
    def _exec_read(self, executor: 'LFIExecutor'): pass
    def _exec_write(self, executor: 'LFIExecutor'): pass
    def _exec_mov(self, executor: 'LFIExecutor'): pass
    def _exec_add(self, executor: 'LFIExecutor'): pass
    def _exec_sub(self, executor: 'LFIExecutor'): pass
    def _exec_inc(self, executor: 'LFIExecutor'): pass
    def _exec_dec(self, executor: 'LFIExecutor'): pass
    def _exec_jmp(self, executor: 'LFIExecutor'):
        # Unconditional jump changes the instruction pointer.
        # We subtract 1 because the main loop will increment it.
        executor.ip = executor.labels[self.args[0]] - 1

    def _exec_cmp(self, executor: 'LFIExecutor'):
        # In this simplified model, we only care about comparing with the halted state.
        # We'll compare a register (arg0) to the special value 'HALTED' (arg1).
        if self.args[1].upper() == 'HALTED':
            reg_name = self.args[0].upper()
            # The result of the comparison is stored in a special register 'CMP'.
            executor.registers['CMP'] = executor.halted

    def _exec_je(self, executor: 'LFIExecutor'):
        # Jump if Equal. This is where the paraconsistency becomes powerful.
        cmp_state = executor.get_register('CMP')

        # If the comparison state is TRUE or BOTH, we take the jump.
        if cmp_state.is_true():
            executor.ip = executor.labels[self.args[0]] - 1

        # If the comparison state is FALSE or BOTH, we *don't* take the jump.
        # Notice that if the state is BOTH, both conditions are met. This creates
        # two "branches" of the execution path in the abstract model.
        # Since we are not building a full state-space explorer, we model this
        # by simply allowing the IP to increment naturally for the 'false' case.
    def _exec_jne(self, executor: 'LFIExecutor'): pass
    def _exec_jg(self, executor: 'LFIExecutor'): pass
    def _exec_jl(self, executor: 'LFIExecutor'): pass
    def _exec_call(self, executor: 'LFIExecutor'): pass


class LFIExecutor:
    """
    A paraconsistent interpreter for UDC plans.

    It models the state of the UDC machine not with concrete values, but with
    ParaconsistentState objects. This allows it to explore the consequences
    of contradictory assumptions.
    """
    def __init__(self, instructions: list, labels: dict):
        self.instructions = [LFIInstruction(i.opcode, i.args) for i in instructions]
        self.labels = labels

        # Paraconsistent VM State
        self.tape = {} # Dict[int, ParaconsistentState]
        self.registers = {} # Dict[str, ParaconsistentState]
        self.ip = 0 # Instruction Pointer (concrete value)
        self.halted = ParaconsistentState(ParaconsistentTruth.FALSE)

        # Analysis metadata
        self.execution_trace = []

    def get_register(self, name: str) -> ParaconsistentState:
        """Gets a register's state, initializing if not present."""
        if name not in self.registers:
            self.registers[name] = ParaconsistentState(ParaconsistentTruth.NEITHER)
        return self.registers[name]

    def run_step(self):
        """Executes a single instruction step."""
        if self.halted.is_true() or self.ip >= len(self.instructions):
            # If any execution path has halted, we stop.
            # In a paraconsistent context, it could be both halted and not.
            if not self.halted.is_true():
                self.halted.value = ParaconsistentTruth.TRUE # End of plan implies halt
            return

        instruction = self.instructions[self.ip]
        self.execution_trace.append(f"IP:{self.ip} - Executing: {instruction}")

        # Execute the instruction, which modifies the paraconsistent state
        instruction.execute(self)

        self.ip += 1 # Move to the next instruction by default


class ParaconsistentHaltingDecider:
    """
    Analyzes a UDC plan using the LFI Executor to determine its
    paraconsistent halting status.
    """
    def __init__(self, plan_path: str, max_steps: int = 100):
        self.plan_path = plan_path
        self.max_steps = max_steps
        self.instructions: list[UDCInstruction] = []
        self.labels: dict[str, int] = {}
        self.executor: LFIExecutor | None = None

    def _parse_plan(self):
        """
        Parses the .udc file into instructions and labels, reusing the logic
        from the heuristic analyzer.
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
                else:
                    self.instructions.append(UDCInstruction(line_num, line_stripped, opcode, args))
                    instruction_index += 1

    def analyze(self) -> ParaconsistentState:
        """
        Runs the analysis and returns the final paraconsistent halting state.
        """
        self._parse_plan()
        self.executor = LFIExecutor(self.instructions, self.labels)

        # This is the core of the paraconsistent analysis.
        # We model the program's behavior under the assumption that it does *not* halt.
        # This is the equivalent of feeding the "program" to itself.
        self.executor.halted = ParaconsistentState(ParaconsistentTruth.FALSE)

        # Now, we run the executor for a number of steps.
        for _ in range(self.max_steps):
            if self.executor.ip >= len(self.executor.instructions):
                # If the program counter goes past the end, it has implicitly halted.
                new_value = self.executor.halted.value.value | {True}
                self.executor.halted.value = ParaconsistentTruth(new_value)
                break
            self.executor.run_step()

        return self.executor.halted