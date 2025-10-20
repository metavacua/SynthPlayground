# System Documentation

---

## `/app/language_theory/toolchain/` Directory

### `/app/language_theory/toolchain/__init__.py`

_No module-level docstring found._

### `/app/language_theory/toolchain/complexity.py`

_No module-level docstring found._


**Public Functions:**


- #### `def main()`

  > Main function for the complexity analyzer.
  > This script takes another Python script and its arguments as input,
  > runs it, and reports the number of instructions executed.



**Public Classes:**


- #### `class ComplexityTracer`

  > A tracer to count Python instructions executed.


  **Methods:**

  - ##### `def __init__(self)`

  - ##### `def run_and_trace(self, target_module_str, script_args)`

    > Runs a target module with tracing enabled using runpy.

  - ##### `def trace_dispatch(self, frame, event, arg)`


### `/app/language_theory/toolchain/grammar.py`

_No module-level docstring found._


**Public Classes:**


- #### `class Grammar`

  > A class to represent a formal grammar. It parses a grammar file
  > and provides helpers for analyzing its properties.


  **Methods:**

  - ##### `def __init__(self, filepath)`

  - ##### `def __str__(self)`

  - ##### `def get_non_terminals(self)`

    > Returns the set of all non-terminal symbols.

  - ##### `def get_productions_dict(self)`

    > Returns productions grouped by LHS, for parser use.

  - ##### `def get_terminals(self)`

    > Returns the set of all terminal symbols.


### `/app/language_theory/toolchain/quantify.py`

_No module-level docstring found._


**Public Functions:**


- #### `def main()`

  > Main function to run the grammar quantifier.
  > This tool computes and reports various metrics for a given grammar.


### `/app/language_theory/toolchain/recognizer.py`

_No module-level docstring found._


**Public Functions:**


- #### `def count_parses(item)`


- #### `def get_parse_count(chart, start_symbol)`


- #### `def main()`


- #### `def print_path(path)`


- #### `def recognize_earley(grammar_productions, start_symbol, input_tokens)`


- #### `def recognize_right_linear(grammar_productions, start_symbol, input_string)`


- #### `def reverse_grammar(grammar_productions)`



**Public Classes:**


- #### `class EarleyItem`


  **Methods:**

  - ##### `def __eq__(self, other)`

  - ##### `def __hash__(self)`

  - ##### `def __init__(self, rule, dot_pos, start_idx)`

  - ##### `def __repr__(self)`


---

## `/app/logic_system/src/` Directory

### `/app/logic_system/src/__init__.py`

_No module-level docstring found._

### `/app/logic_system/src/diagram.py`

_No module-level docstring found._


**Public Classes:**


- #### `class Diagram`


  **Methods:**

  - ##### `def __init__(self)`

  - ##### `def find_path(self, start, end)`

    > Finds a path of translations from a start logic to an end logic using BFS.

  - ##### `def translate(self, proof, start, end)`

    > Translates a proof from a starting logic to an ending logic.


- #### `class Logic`


### `/app/logic_system/src/formulas.py`

_No module-level docstring found._


**Public Classes:**


- #### `class And`


  **Methods:**

  - ##### `def __repr__(self)`


- #### `class BinaryOp`


  **Methods:**

  - ##### `def __init__(self, left, right)`


- #### `class Formula`


  **Methods:**

  - ##### `def __eq__(self, other)`

  - ##### `def __hash__(self)`

  - ##### `def __repr__(self)`


- #### `class Implies`


  **Methods:**

  - ##### `def __repr__(self)`


- #### `class LinImplies`


  **Methods:**

  - ##### `def __repr__(self)`


- #### `class Not`


  **Methods:**

  - ##### `def __repr__(self)`


- #### `class OfCourse`


  **Methods:**

  - ##### `def __repr__(self)`


- #### `class Or`


  **Methods:**

  - ##### `def __repr__(self)`


- #### `class Par`


  **Methods:**

  - ##### `def __repr__(self)`


- #### `class Plus`

  > Additive Disjunction


  **Methods:**

  - ##### `def __repr__(self)`


- #### `class Prop`


  **Methods:**

  - ##### `def __init__(self, name)`

  - ##### `def __repr__(self)`


- #### `class Tensor`


  **Methods:**

  - ##### `def __repr__(self)`


- #### `class UnaryOp`


  **Methods:**

  - ##### `def __init__(self, operand)`


- #### `class With`

  > Additive Conjunction


  **Methods:**

  - ##### `def __repr__(self)`


### `/app/logic_system/src/ill.py`

Implementation of Intuitionistic Linear Logic (ILL).

The logic and rule formulations in this module are heavily based on the
formalization found in the "Deep Embedding of Intuitionistic Linear Logic"
entry in the Archive of Formal Proofs by Filip Smola and Jacques D. Fleuriot.

The original work can be found at:
https://www.isa-afp.org/entries/ILL.html

The use of this work is subject to the terms of the BSD license, a copy of
which is included in this project as ISABELLE_LICENSE.


**Public Functions:**


- #### `def axiom(A)`

  > A ⊢ A


- #### `def contraction(proof, formula)`

  > Γ, !A, !A ⊢ B
  > ----------------
  >    Γ, !A ⊢ B


- #### `def cut(left_proof, right_proof)`

  > Γ ⊢ A   and   Δ, A ⊢ C
  > --------------------------
  >      Γ, Δ ⊢ C


- #### `def dereliction(proof, formula)`

  > Γ, A ⊢ B
  > ------------
  > Γ, !A ⊢ B


- #### `def lin_implies_left(left_proof, right_proof, formula)`

  > Γ ⊢ A   and   Δ, B ⊢ C
  > --------------------------
  >    Γ, Δ, A ⊸ B ⊢ C


- #### `def lin_implies_right(proof, formula)`

  > Γ, A ⊢ B
  > ------------
  > Γ ⊢ A ⊸ B


- #### `def of_course_right(proof)`

  > !Γ ⊢ A
  > ----------
  > !Γ ⊢ !A


- #### `def plus_left(left_proof, right_proof, formula)`

  > Γ, A ⊢ C   and   Γ, B ⊢ C
  > --------------------------
  >      Γ, A ⊕ B ⊢ C


- #### `def plus_right_1(proof, formula)`

  > Γ ⊢ A
  > ------------
  > Γ ⊢ A ⊕ B


- #### `def plus_right_2(proof, formula)`

  > Γ ⊢ B
  > ------------
  > Γ ⊢ A ⊕ B


- #### `def tensor_left(proof, formula)`

  > Γ, A, B ⊢ C
  > ---------------
  >  Γ, A ⊗ B ⊢ C


- #### `def tensor_right(left_proof, right_proof)`

  > Γ ⊢ A   and   Δ ⊢ B
  > -----------------------
  >      Γ, Δ ⊢ A ⊗ B


- #### `def weakening(proof, formula)`

  > Γ ⊢ B
  > ------------
  > Γ, !A ⊢ B


- #### `def with_left_1(proof, formula)`

  > Γ, A ⊢ C
  > ------------
  > Γ, A & B ⊢ C


- #### `def with_left_2(proof, formula)`

  > Γ, B ⊢ C
  > ------------
  > Γ, A & B ⊢ C


- #### `def with_right(left_proof, right_proof)`

  > Γ ⊢ A   and   Γ ⊢ B
  > -----------------------
  >       Γ ⊢ A & B



**Public Classes:**


- #### `class ILLSequent`


  **Methods:**

  - ##### `def __init__(self, antecedent, succedent)`

  - ##### `def __repr__(self)`

  - ##### `def succedent_formula(self)`


### `/app/logic_system/src/lj.py`

_No module-level docstring found._


**Public Functions:**


- #### `def and_left(proof, formula)`

  > Γ, A, B ⊢ Δ / Γ, A ∧ B ⊢ Δ


- #### `def and_right(left_proof, right_proof)`

  > Γ ⊢ A   and   Γ ⊢ B / Γ ⊢ A ∧ B


- #### `def axiom(A)`

  > A ⊢ A


- #### `def cut(left_proof, right_proof, formula)`

  > Γ ⊢ A   and   A, Γ' ⊢ B / Γ, Γ' ⊢ B


- #### `def implies_left(left_proof, right_proof, formula)`

  > Γ ⊢ A   and   B, Γ' ⊢ C / A → B, Γ, Γ' ⊢ C


- #### `def implies_right(proof, formula)`

  > A, Γ ⊢ B / Γ ⊢ A → B


- #### `def not_left(proof, formula)`

  > Γ ⊢ A / ¬A, Γ ⊢


- #### `def not_right(proof, formula)`

  > A, Γ ⊢ / Γ ⊢ ¬A


- #### `def or_left(left_proof, right_proof, formula)`

  > Γ, A ⊢ Δ   and   Γ, B ⊢ Δ / Γ, A ∨ B ⊢ Δ


- #### `def or_right(proof, formula)`

  > Γ ⊢ A / Γ ⊢ A ∨ B  or  Γ ⊢ B / Γ ⊢ A ∨ B


- #### `def weak_left(proof, formula)`

  > Γ ⊢ Δ  /  Γ, A ⊢ Δ



**Public Classes:**


- #### `class LJSequent`


  **Methods:**

  - ##### `def __init__(self, antecedent, succedent=None)`

  - ##### `def __repr__(self)`

  - ##### `def succedent_formula(self)`


### `/app/logic_system/src/lk.py`

_No module-level docstring found._


**Public Functions:**


- #### `def and_left(proof, formula)`

  > Γ, A, B ⊢ Δ / Γ, A ∧ B ⊢ Δ


- #### `def and_right(left_proof, right_proof)`

  > Γ ⊢ Δ, A   and   Γ ⊢ Δ, B / Γ ⊢ Δ, A ∧ B


- #### `def axiom(A)`

  > A ⊢ A


- #### `def implies_left(left_proof, right_proof, formula)`

  > Γ ⊢ Δ, A   and   B, Γ ⊢ Δ / A → B, Γ ⊢ Δ


- #### `def implies_right(proof, formula)`

  > A, Γ ⊢ Δ, B / Γ ⊢ Δ, A → B


- #### `def not_left(proof, formula)`

  > Γ ⊢ Δ, A / ¬A, Γ ⊢ Δ


- #### `def not_right(proof, formula)`

  > A, Γ ⊢ Δ / Γ ⊢ Δ, ¬A


- #### `def or_left(left_proof, right_proof)`

  > Γ, A ⊢ Δ   and   Γ, B ⊢ Δ / Γ, A ∨ B ⊢ Δ


- #### `def or_right(proof, formula)`

  > Γ ⊢ Δ, A, B / Γ ⊢ Δ, A ∨ B


- #### `def weak_left(proof, formula)`

  > Γ ⊢ Δ  /  Γ, A ⊢ Δ


- #### `def weak_right(proof, formula)`

  > Γ ⊢ Δ  /  Γ ⊢ Δ, A


### `/app/logic_system/src/ll.py`

_No module-level docstring found._


**Public Functions:**


- #### `def axiom(A)`

  > A ⊢ A


- #### `def cut(left_proof, right_proof)`

  > Γ ⊢ Δ, A   and   A, Γ' ⊢ Δ'
  > --------------------------------
  >          Γ, Γ' ⊢ Δ, Δ'


- #### `def par_left(left_proof, right_proof, formula)`

  > Γ, A ⊢ Δ   and   Γ', B ⊢ Δ'
  > --------------------------------
  >       Γ, Γ', A ⅋ B ⊢ Δ, Δ'


- #### `def par_right(proof, formula)`

  > Γ ⊢ Δ, A, B
  > ---------------
  >  Γ ⊢ Δ, A ⅋ B


- #### `def tensor_left(proof, formula)`

  > Γ, A, B ⊢ Δ
  > ---------------
  >  Γ, A ⊗ B ⊢ Δ


- #### `def tensor_right(left_proof, right_proof, formula)`

  > Γ ⊢ Δ, A   and   Γ' ⊢ Δ', B
  > --------------------------------
  >       Γ, Γ' ⊢ Δ, Δ', A ⊗ B


### `/app/logic_system/src/proof.py`

_No module-level docstring found._


**Public Classes:**


- #### `class ProofTree`


  **Methods:**

  - ##### `def __init__(self, conclusion, rule, premises=None)`

  - ##### `def __repr__(self, level=0)`

  - ##### `def to_dict(self)`

    > Serializes the proof tree to a dictionary.


- #### `class Rule`


  **Methods:**

  - ##### `def __init__(self, name)`

  - ##### `def __repr__(self)`


### `/app/logic_system/src/sequents.py`

_No module-level docstring found._


**Public Classes:**


- #### `class Sequent`


  **Methods:**

  - ##### `def __eq__(self, other)`

  - ##### `def __hash__(self)`

  - ##### `def __init__(self, antecedent, succedent)`

  - ##### `def __repr__(self)`


### `/app/logic_system/src/synthesizer.py`

_No module-level docstring found._


**Public Classes:**


- #### `class Synthesizer`


  **Methods:**

  - ##### `def __init__(self, logic_module=ill)`

  - ##### `def synthesize(self, goal, max_depth=10, visited=None)`


### `/app/logic_system/src/translations.py`

_No module-level docstring found._


**Public Functions:**


- #### `def bang_context(context)`

  > Applies ! to every formula in a context.


- #### `def ill_to_ll(ill_proof)`

  > Translates a proof from the ILL calculus to the LL calculus.
  > This is a direct embedding, as any valid ILL proof is also a valid LL proof.


- #### `def lj_to_ill_proof(lj_proof)`

  > Translates a full proof from LJ to ILL.
  > A proof of Γ ⊢ A in LJ becomes a proof of !Γ* ⊢ A* in ILL.


- #### `def lj_to_lk(lj_proof)`

  > Translates a proof from the LJ calculus to the LK calculus.
  > This is a direct embedding, as any valid LJ proof is also a valid LK proof.


- #### `def translate_formula_lj_to_ill(formula)`

  > Translates a formula from Intuitionistic Logic (LJ) to Intuitionistic Linear Logic (ILL)
  > using a standard Girard-style translation.


---

## `/app/tooling/` Directory

### `/app/tooling/__init__.py`

_No module-level docstring found._

### `/app/tooling/agent_shell.py`

The new, interactive, API-driven entry point for the agent.

This script replaces the old file-based signaling system with a direct,
programmatic interface to the MasterControlGraph FSM. It is responsible for:
1.  Initializing the agent's state and a centralized logger.
2.  Instantiating and running the MasterControlGraph.
3.  Driving the FSM by calling its methods and passing data and the logger.
4.  Containing the core "agent logic" (e.g., an LLM call) to generate plans
    and respond to requests for action.


**Public Functions:**


- #### `def find_fsm_transition(fsm, source_state, trigger)`

  > Finds the destination state for a given source and trigger.


- #### `def load_tools_from_manifest(manifest_path='tooling/tool_manifest.json')`

  > Loads tools from the tool manifest.


- #### `def main()`

  > Main entry point for the agent shell.


- #### `def run_agent_loop(task_description, tools, model=None, plan_content=None)`

  > The main loop that drives the agent's lifecycle via the FSM.


### `/app/tooling/appl_runner.py`

A command-line tool for executing APPL files.

This script provides a simple interface to run APPL files using the main
`run.py` interpreter. It captures and prints the output of the execution,
and provides detailed error reporting if the execution fails.


**Public Functions:**


- #### `def main()`

  > Main function to run the APPL runner from the command line.


- #### `def run_appl_file(filepath)`

  > Executes an APPL file using the run.py interpreter.
  >
  > Args:
  >     filepath: The path to the .appl file to execute.
  >
  > Returns:
  >     The output from the APPL interpreter.


### `/app/tooling/appl_to_lfi_ill.py`

A compiler that translates APPL (a simple functional language) to LFI-ILL.

This script takes a Python file containing an APPL AST, and compiles it into
an LFI-ILL AST. The resulting AST is then written to a `.lfi_ill` file.


**Public Functions:**


- #### `def main()`



**Public Classes:**


- #### `class ApplToLfiIllCompiler`


  **Methods:**

  - ##### `def __init__(self)`

  - ##### `def compile(self, appl_node)`

    > Recursively walks the APPL AST and translates it to an LFI ILL AST.

  - ##### `def compile_type(self, type_)`

    > Translates APPL types to LFI ILL types.


### `/app/tooling/auditor.py`

A unified auditing tool for maintaining repository health and compliance.

This script combines the functionality of several disparate auditing tools into a
single, comprehensive command-line interface. It serves as the central tool for
validating the key components of the agent's architecture, including protocols,
plans, and documentation.

The auditor can perform the following checks:
1.  **Protocol Audit (`protocol`):**
    - Checks if `AGENTS.md` artifacts are stale compared to their source files.
    - Verifies protocol completeness by comparing tools used in logs against
      tools defined in protocols.
    - Analyzes tool usage frequency (centrality).
2.  **Plan Registry Audit (`plans`):**
    - Scans `knowledge_core/plan_registry.json` for "dead links" where the
      target plan file does not exist.
3.  **Documentation Audit (`docs`):**
    - Scans the generated `SYSTEM_DOCUMENTATION.md` to find Python modules
      that are missing module-level docstrings.

The tool is designed to be run from the command line and can execute specific
audits or all of them, generating a consolidated `audit_report.md` file.


**Public Functions:**


- #### `def find_all_agents_md_files(root_dir)`


- #### `def get_protocol_tools_from_agents_md(agents_md_paths)`


- #### `def get_used_tools_from_log(log_path)`


- #### `def main()`


- #### `def run_doc_audit()`


- #### `def run_plan_registry_audit()`


- #### `def run_protocol_audit()`


### `/app/tooling/aura_executor.py`

This script serves as the command-line executor for `.aura` files.

It bridges the gap between the high-level Aura scripting language and the
agent's underlying Python-based toolset. The executor is responsible for:
1.  Parsing the `.aura` source code using the lexer and parser from the
    `aura_lang` package.
2.  Setting up an execution environment for the interpreter.
3.  Injecting a "tool-calling" capability into the Aura environment, which
    allows Aura scripts to dynamically invoke registered Python tools
    (e.g., `hdl_prover`, `environmental_probe`).
4.  Executing the parsed program and printing the final result.

This makes it a key component for enabling more expressive and complex
automation scripts for the agent.


**Public Functions:**


- #### `def dynamic_agent_call_tool(tool_name_obj, *args)`

  > Dynamically imports and calls a tool from the 'tooling' directory and wraps the result.
  >
  > This function provides the bridge between the Aura scripting environment and the
  > Python-based agent tools. It takes the tool's module name and arguments,
  > runs the tool in a subprocess, and wraps the captured output in an Aura `Object`.
  >
  > Args:
  >     tool_name_obj: An Aura Object containing the tool's module name (e.g., 'hdl_prover').
  >     *args: A variable number of Aura Objects to be passed as string arguments to the tool.
  >
  > Returns:
  >     An Aura `Object` containing the tool's stdout as a string, or an error message.


- #### `def main()`

  > Main entry point for the Aura script executor.


### `/app/tooling/aura_to_lfi_ill.py`

A compiler that translates AURA code to LFI-ILL.

This script takes an AURA file, parses it, and compiles it into an LFI-ILL
AST. The resulting AST is then written to a `.lfi_ill` file.


**Public Functions:**


- #### `def main()`



**Public Classes:**


- #### `class AuraToLfiIllCompiler`


  **Methods:**

  - ##### `def __init__(self)`

  - ##### `def compile(self, node)`

  - ##### `def compile_BlockStatement(self, node)`

  - ##### `def compile_CallExpression(self, node)`

  - ##### `def compile_ExpressionStatement(self, node)`

  - ##### `def compile_ForStatement(self, node)`

  - ##### `def compile_FunctionDefinition(self, node)`

  - ##### `def compile_Identifier(self, node)`

  - ##### `def compile_IfStatement(self, node)`

  - ##### `def compile_InfixExpression(self, node)`

  - ##### `def compile_IntegerLiteral(self, node)`

  - ##### `def compile_LetStatement(self, node)`

  - ##### `def compile_PrintStatement(self, node)`

  - ##### `def compile_Program(self, node)`

  - ##### `def compile_ReturnStatement(self, node)`

  - ##### `def compile_StringLiteral(self, node)`

  - ##### `def generic_compiler(self, node)`


### `/app/tooling/autonomous_agent.py`

_No module-level docstring found._


**Public Functions:**


- #### `def main()`



**Public Classes:**


- #### `class AutonomousAgent`


  **Methods:**

  - ##### `def __init__(self, task)`

  - ##### `def execute_plan(self)`

    > Executes the generated plan.

  - ##### `def generate_plan(self)`

    > Generates a plan to accomplish the task.

  - ##### `def run(self)`

    > Runs the agent's main loop.


### `/app/tooling/background_researcher.py`

This script performs a simulated research task in the background.
It takes a task ID as a command-line argument and writes its findings
to a temporary file that the main agent can poll.


**Public Functions:**


- #### `def perform_research(task_id)`

  > Simulates a research task and writes the result to a file.


### `/app/tooling/bash_runner.py`

_No module-level docstring found._


**Public Functions:**


- #### `def run_in_bash_session(command)`

  > Runs the given bash command in the sandbox.


### `/app/tooling/build_utils.py`

_No module-level docstring found._


**Public Functions:**


- #### `def execute_code(code, protocol_id, rule_id)`

  > Executes a block of Python code in a controlled environment.


- #### `def find_files(pattern, base_dir='.', recursive=True)`

  > Finds files matching a pattern in a directory.


- #### `def load_schema(schema_file)`

  > Loads the JSON schema from a file.


- #### `def sanitize_markdown(content)`

  > Removes potentially unsafe constructs from Markdown.


### `/app/tooling/builder.py`

A unified, configuration-driven build script for the project.

This script serves as the central entry point for all build-related tasks, such
as generating documentation, compiling protocols, and running code quality checks.
It replaces a traditional Makefile's direct command execution with a more
structured, maintainable, and introspectable approach.

The core logic is driven by a `build_config.json` file, which defines a series
of "targets." Each target specifies:
- The `type` of target: "compiler" or "command".
- For "compiler" types: `compiler` script, `output`, `sources`, and `options`.
- For "command" types: the `command` to execute.

The configuration also defines "build_groups", which are ordered collections of
targets (e.g., "all", "quality").

This centralized builder provides several advantages:
- **Single Source of Truth:** The `build_config.json` file is the definitive
  source for all build logic.
- **Consistency:** Ensures all build tasks are executed in a uniform way.
- **Extensibility:** New build targets can be added by simply updating the
  configuration file.
- **Discoverability:** The script can list all available targets and groups.


**Public Functions:**


- #### `def execute_build(target_name, config)`

  > Executes the build process for a specific target.


- #### `def execute_command_target(target_name, target_config)`

  > Executes a 'command' type build target.


- #### `def execute_compiler_target(target_name, target_config)`

  > Executes a 'compiler' type build target.


- #### `def load_config()`

  > Loads the build configuration file.


- #### `def main()`

  > Main function to parse arguments and drive the build process.


### `/app/tooling/capability_verifier.py`

A tool to verify that the agent can monotonically improve its capabilities.

This script is designed to provide a formal, automated test for the agent's
self-correction and learning mechanisms. It ensures that when the agent learns
a new capability, it does so without losing (regressing) any of its existing
capabilities. This is a critical safeguard for ensuring robust and reliable
agent evolution.

The tool works by orchestrating a four-step process:
1.  **Confirm Initial Failure:** It runs a specific test file that is known to
    fail, verifying that the agent currently lacks the target capability.
2.  **Invoke Self-Correction:** It simulates the discovery of a new "lesson" and
    triggers the `self_correction_orchestrator.py` script, which is responsible
    for integrating new knowledge and skills.
3.  **Confirm Final Success:** It runs the same test file again, confirming that
    the agent has successfully learned the new capability and the test now passes.
4.  **Check for Regressions:** It runs the full, existing test suite to ensure
    that the process of learning the new skill has not inadvertently broken any
    previously functional capabilities.

This provides a closed-loop verification of monotonic improvement, which is a
cornerstone of the agent's design philosophy.


**Public Functions:**


- #### `def main()`

  > A tool to verify that the agent can monotonically improve its capabilities.
  >
  > This tool works by:
  > 1. Running a target test file that is known to fail, confirming the agent lacks a capability.
  > 2. Invoking the agent's self-correction mechanism to learn the new capability.
  > 3. Running the target test again to confirm it now passes.
  > 4. Running the full test suite to ensure no existing capabilities were lost.


### `/app/tooling/code_suggester.py`

Handles the generation and application of autonomous code change suggestions.

This tool is a key component of the advanced self-correction loop. It is
designed to be invoked by the self-correction orchestrator when a lesson
contains a 'propose-code-change' action.

For its initial implementation, this tool acts as a structured executor. It
takes a lesson where the 'details' field contains a fully-formed git-style
merge diff and applies it to the target file. It does this by generating a
temporary, single-step plan file and signaling its location for the master
controller to execute.

This establishes the fundamental workflow for autonomous code modification,
decoupling the suggestion logic from the execution logic. Future iterations
can enhance this tool with more sophisticated code generation capabilities
(e.g., using an LLM to generate the diff from a natural language description)
without altering the core orchestration process.


**Public Functions:**


- #### `def generate_suggestion_plan(filepath, diff_content)`

  > Generates a temporary, single-step plan file to apply a code change.
  >
  > Args:
  >     filepath: The path to the file that needs to be modified.
  >     diff_content: The git-style merge diff block to be applied.
  >
  > Returns:
  >     The path to the generated temporary plan file.


- #### `def main()`

  > Main entry point for the code suggester tool.
  > Parses arguments, generates a plan, and prints the plan's path to stdout.


### `/app/tooling/compile_protocols.py`

_No module-level docstring found._


**Public Functions:**


- #### `def compile_module(module_dir)`

  > Compiles the protocol files in a directory into a single AGENTS.md.


- #### `def main()`

  > Main function to find and compile all protocol modules.


### `/app/tooling/context_awareness_scanner.py`

A tool for performing static analysis on a Python file to understand its context.

This script provides a "contextual awareness" scan of a specified Python file
to help an agent (or a human) understand its role, dependencies, and connections
within a larger codebase. This is crucial for planning complex changes or
refactoring efforts, as it provides a snapshot of the potential impact of
modifying a file.

The scanner performs three main functions:
1.  **Symbol Definition Analysis:** It uses Python's Abstract Syntax Tree (AST)
    module to parse the target file and identify all the functions and classes
    that are defined within it.
2.  **Import Analysis:** It also uses the AST to find all modules and symbols
    that the target file imports, revealing its dependencies on other parts of
    the codebase or external libraries.
3.  **Reference Finding:** It performs a repository-wide search to find all other
    files that reference the symbols defined in the target file. This helps to
    understand how the file is used by the rest of the system.

The final output is a detailed JSON report containing all of this information,
which can be used as a foundational artifact for automated planning or human review.


**Public Functions:**


- #### `def find_references(symbol_name, search_path)`

  > Finds all files in a directory that reference a given symbol.


- #### `def get_defined_symbols(filepath)`

  > Parses a Python file to find all defined functions and classes.


- #### `def get_imported_symbols(filepath)`

  > Parses a Python file to find all imported modules and symbols.


- #### `def main()`


### `/app/tooling/csdc_cli.py`

A command-line tool for managing the Context-Sensitive Development Cycle (CSDC).

This script provides an interface to validate a development plan against a specific
CSDC model (A or B) and a given complexity class (P or EXP). It ensures that a
plan adheres to the strict logical and computational constraints defined by the
CSDC protocol before it is executed.

The tool performs two main checks:
1.  **Complexity Analysis:** It analyzes the plan to determine its computational
    complexity and verifies that it matches the expected complexity class.
2.  **Model Validation:** It validates the plan's commands against the rules of
    the specified CSDC model, ensuring that it does not violate any of the
    model's constraints (e.g., forbidding certain functions).

This serves as a critical gateway for ensuring that all development work within
the CSDC framework is sound, predictable, and compliant with the governing
meta-mathematical principles.


**Public Functions:**


- #### `def main()`


### `/app/tooling/dependency_graph_generator.py`

Scans the repository for dependency files and generates a unified dependency graph.

This script is a crucial component of the agent's environmental awareness,
providing a clear map of the software supply chain. It recursively searches the
entire repository for common dependency management files, specifically:
- `package.json` (for JavaScript/Node.js projects)
- `requirements.txt` (for Python projects)

It parses these files to identify two key types of relationships:
1.  **Internal Dependencies:** Links between different projects within this repository.
2.  **External Dependencies:** Links to third-party libraries and packages.

The final output is a JSON file, `knowledge_core/dependency_graph.json`, which
represents these relationships as a graph structure with nodes (projects and
dependencies) and edges (the dependency links). This artifact is a primary
input for the agent's orientation and planning phases, allowing it to reason
about the potential impact of its changes.


**Public Functions:**


- #### `def find_dependency_files(root_dir)`

  > Finds all package.json and requirements.txt files, excluding node_modules.


- #### `def generate_dependency_graph(root_dir='.')`

  > Generates a dependency graph for all supported dependency files found.


- #### `def main()`

  > Main function to generate and save the dependency graph.


- #### `def parse_package_json(package_json_path)`

  > Parses a single package.json file to extract its name and dependencies.


- #### `def parse_requirements_txt(requirements_path, root_dir)`

  > Parses a requirements.txt file to extract its dependencies.


### `/app/tooling/doc_builder.py`

A unified documentation builder for the project.
...


**Public Functions:**


- #### `def find_python_files(directories)`


- #### `def format_args(args)`


- #### `def generate_documentation_for_module(mod_doc)`


- #### `def generate_pages(readme_path, agents_md_path, output_file)`

  > Generates the index.html for GitHub Pages.


- #### `def generate_readme(agents_md_path, output_file)`

  > Generates the high-level README.md for a module.


- #### `def generate_system_docs(source_dirs, output_file)`

  > Generates the detailed SYSTEM_DOCUMENTATION.md.


- #### `def generate_tool_readme(source_file, output_file)`

  > Generates a README.md for a single tool from its docstring.


- #### `def generate_tooling_readme(source_dir, output_file)`

  > Generates a single README.md for the tooling directory.


- #### `def get_module_docstring(filepath)`

  > Parses a Python file and extracts its module-level docstring.


- #### `def get_protocol_summary(agents_md_path)`

  > Parses an AGENTS.md file and extracts a list of protocol summaries.


- #### `def main()`


- #### `def parse_file_for_docs(filepath)`



**Public Classes:**


- #### `class ClassDoc`


  **Methods:**

  - ##### `def __init__(self, name, docstring, methods)`


- #### `class DocVisitor`


  **Methods:**

  - ##### `def __init__(self)`

  - ##### `def visit_ClassDef(self, node)`

  - ##### `def visit_FunctionDef(self, node)`


- #### `class FunctionDoc`


  **Methods:**

  - ##### `def __init__(self, name, signature, docstring)`


- #### `class ModuleDoc`


  **Methods:**

  - ##### `def __init__(self, name, docstring, classes, functions)`


### `/app/tooling/document_scanner.py`

A tool for scanning the repository for human-readable documents and extracting their text content.

This script is a crucial component of the agent's initial information-gathering
and orientation phase. It allows the agent to ingest knowledge from unstructured
or semi-structured documents that are not part of the formal codebase, but which
may contain critical context, requirements, or specifications.

The scanner searches a given directory for files with common document extensions:
- `.pdf`: Uses the Gemini API to extract text and understand the content of PDF files.
- `.md`: Reads Markdown files.
- `.txt`: Reads plain text files.

The output is a dictionary where the keys are the file paths of the discovered
documents and the values are their extracted text content. This data can then
be used by the agent to inform its planning and execution process. This tool
is essential for bridging the gap between human-written documentation and the
agent's operational awareness.


**Public Functions:**


- #### `def scan_documents(directory='.')`

  > Scans a directory for PDF, Markdown, and text files and extracts their content.


### `/app/tooling/environmental_probe.py`

Performs a series of checks to assess the capabilities of the execution environment.

This script is a critical diagnostic tool run at the beginning of a task to
ensure the agent understands its operational sandbox. It verifies fundamental
capabilities required for most software development tasks:

1.  **Filesystem I/O:** Confirms that the agent can create, write to, read from,
    and delete files. It also provides a basic latency measurement for these
    operations.
2.  **Network Connectivity:** Checks for external network access by attempting to
    connect to a highly-available public endpoint (google.com). This is crucial
    for tasks requiring `git` operations, package downloads, or API calls.
3.  **Environment Variables:** Verifies that standard environment variables are
    accessible, which is a prerequisite for many command-line tools.

The script generates a human-readable report summarizing the results of these
probes, allowing the agent to quickly identify any environmental constraints
that might impact its ability to complete a task.


**Public Functions:**


- #### `def main()`

  > Runs all environmental probes and prints a summary report.


- #### `def probe_environment_variables()`

  > Checks for the presence of a common environment variable.


- #### `def probe_filesystem()`

  > Tests file system write/read/delete capabilities and measures latency.


- #### `def probe_network()`

  > Tests network connectivity and measures latency to a reliable external endpoint.


### `/app/tooling/external_api_client.py`

A standardized client for interacting with external agent APIs.


**Public Classes:**


- #### `class ExternalApiClient`


  **Methods:**

  - ##### `def __init__(self, api_name, api_key_env_var)`

  - ##### `def get(self, endpoint, params=None)`

    > Sends a GET request to the specified endpoint.

  - ##### `def post(self, endpoint, data)`

    > Sends a POST request to the specified endpoint.


### `/app/tooling/fdc_cli.py`

This script provides a command-line interface (CLI) for managing the Finite
Development Cycle (FDC).

The FDC is a structured workflow for agent-driven software development. This CLI
is the primary human interface for interacting with that cycle, providing
commands to:
- **start:** Initiates a new development task, triggering the "Advanced
  Orientation and Research Protocol" (AORP) to ensure the agent is fully
  contextualized.
- **close:** Formally concludes a task, creating a post-mortem template for
  analysis and lesson-learning.
- **validate:** Checks a given plan file for both syntactic and semantic
  correctness against the FDC's governing Finite State Machine (FSM). This
  ensures that a plan is executable and will not violate protocol.
- **analyze:** Examines a plan to determine its computational complexity (e.g.,
  Constant, Polynomial, Exponential) and its modality (Read-Only vs.
  Read-Write), providing insight into the plan's potential impact.


**Public Functions:**


- #### `def analyze_plan(plan_filepath, return_results=False)`

  > Analyzes a plan file to determine its complexity class and modality.


- #### `def close_task(task_id)`

  > Automates the closing of a Finite Development Cycle.


- #### `def main()`


- #### `def start_task(task_id)`

  > Initiates the AORP cascade for a new task.


- #### `def validate_plan(plan_filepath)`


### `/app/tooling/file_reader.py`

_No module-level docstring found._


**Public Functions:**


- #### `def read_file(filepath)`

  > Reads the content of the specified file.


### `/app/tooling/filesystem_lister.py`

A tool for listing files and directories in a repository, with an option to respect .gitignore.


**Public Functions:**


- #### `def list_all_files_and_dirs(root_dir='.', use_gitignore=True)`

  > Walks through a directory and its subdirectories and returns a sorted list of all
  > files and directories.
  >
  > Args:
  >     root_dir (str): The root directory to start the walk from.
  >     use_gitignore (bool): If True, respects the patterns in the .gitignore file.


### `/app/tooling/gemini_computer_use.py`

A tool for controlling a web browser using the Gemini Computer Use API.

This tool allows the agent to perform tasks like data entry, automated testing,
and web research by controlling a web browser. It uses the Gemini Computer Use
API to "see" the screen and "act" by generating UI actions like mouse clicks
and keyboard inputs.


**Public Functions:**


- #### `def denormalize_x(x, screen_width)`

  > Convert normalized x coordinate (0-1000) to actual pixel coordinate.


- #### `def denormalize_y(y, screen_height)`

  > Convert normalized y coordinate (0-1000) to actual pixel coordinate.


- #### `def execute_function_calls(candidate, page, screen_width, screen_height)`


- #### `def get_function_responses(page, results)`


- #### `def main()`

  > The main entry point for the GeminiComputerUse tool.


### `/app/tooling/halting_heuristic_analyzer.py`

A static analysis tool to estimate the termination risk of a UDC plan.

This script reads a `.udc` plan file, parses its instructions, and uses a
series of heuristics to identify potential infinite loops. It is not a
formal decider (as the halting problem is undecidable), but rather a
practical tool to flag common patterns that lead to non-termination.

The analysis focuses on:
1.  Detecting backward jumps, which are the primary indicator of loops.
2.  Analyzing the exit conditions of these loops (e.g., `JE`, `JNE`).
3.  Checking if the registers involved in the exit conditions are modified
    within the loop body in a way that is likely to lead to termination.

The tool outputs a JSON report detailing the estimated risk level (LOW,
MEDIUM, HIGH) and the specific loops that were identified.


**Public Functions:**


- #### `def main()`

  > Main entry point for the command-line tool.



**Public Classes:**


- #### `class HaltingHeuristicAnalyzer`

  > Performs static analysis on a UDC plan to provide a heuristic-based
  > estimate of its likelihood to terminate.


  **Methods:**

  - ##### `def __init__(self, plan_path)`

  - ##### `def analyze(self)`

    > Runs the full analysis pipeline and returns a report.


- #### `class Instruction`


- #### `class Loop`


### `/app/tooling/hdl_prover.py`

A command-line tool for proving sequents in Intuitionistic Linear Logic.

This script provides a basic interface to a simple logic prover. It takes a
sequent as a command-line argument, parses it into a logical structure, and
then attempts to prove it using a rudimentary proof search algorithm.

The primary purpose of this tool is to allow the agent to perform formal
reasoning and verification tasks by checking the validity of logical entailments.
For example, it can be used to verify that a certain conclusion follows from a
set of premises according to the rules of linear logic.

The current implementation uses a very basic parser and proof algorithm,
serving as a placeholder and demonstration for a more sophisticated, underlying
logic engine.


**Public Functions:**


- #### `def main()`


- #### `def parse_formula(s)`

  > A very basic parser for formulas.


- #### `def parse_sequent(s)`

  > A very basic parser for sequents.


- #### `def prove_sequent(sequent)`

  > A very simple proof search algorithm.
  > This is a placeholder for a more sophisticated prover.


### `/app/tooling/knowledge_compiler.py`

Extracts structured lessons from post-mortem reports and compiles them into a
centralized, long-term knowledge base.

This script is a core component of the agent's self-improvement feedback loop.
After a task is completed, a post-mortem report is generated that includes a
section for "Corrective Actions & Lessons Learned." This script automates the
process of parsing that section to extract key insights.

It identifies pairs of "Lesson" and "Action" statements and transforms them
into a standardized, machine-readable format. These formatted entries are then
appended to the `knowledge_core/lessons.jsonl` file, which serves as the
agent's persistent memory of what has worked, what has failed, and what can be
improved in future tasks.

The script is executed via the command line, taking the path to a completed
post-mortem file as its primary argument.


**Public Functions:**


- #### `def extract_lessons_from_postmortem(postmortem_content)`

  > Parses a post-mortem report to extract lessons learned.
  > Handles multiple possible section headers and formats.


- #### `def extract_metadata_from_postmortem(postmortem_content)`

  > Parses a post-mortem report to extract metadata like Task ID and Date.


- #### `def format_lesson_entry(metadata, lesson_data)`

  > Formats an extracted lesson into a structured JSON object.


- #### `def main()`


- #### `def parse_action_to_command(action_text)`

  > Parses a natural language action string into a machine-executable command.
  >
  > This is the core of translating insights into automated actions. It uses
  > pattern matching to identify specific, supported commands.


- #### `def process_postmortem_file(filepath)`

  > Reads a single post-mortem file and returns its lessons.


### `/app/tooling/knowledge_integrator.py`

A tool for integrating knowledge from various sources across the repository into a single, unified knowledge base.


**Public Functions:**


- #### `def integrate_lessons(graph, lessons_file)`

  > Integrates lessons from a JSONL file into the knowledge graph.


- #### `def integrate_protocols(graph, protocols_dir)`

  > Integrates protocol definitions into the knowledge graph.


- #### `def integrate_research(graph, research_dir)`

  > Integrates research findings into the knowledge graph.


- #### `def main()`


### `/app/tooling/lba_validator.py`

A Linear Bounded Automaton (LBA) for validating Context-Sensitive Development Cycle (CSDC) plans.

This module implements a validator that enforces the context-sensitive rules of the CSDC.
Unlike a simple FSM, an LBA can inspect the entire input "tape" (the plan) to make
validation decisions. This is necessary to enforce rules where the validity of one
command depends on the presence or absence of another command elsewhere in the plan.

The CSDC defines two mutually exclusive models:
- Model A: Permits `define_set_of_names`, but forbids `define_diagonalization_function`.
- Model B: Permits `define_diagonalization_function`, but forbids `define_set_of_names`.

This validator checks for these co-occurrence constraints.


**Public Classes:**


- #### `class LBAValidator`

  > A validator that uses LBA principles to enforce CSDC rules.


  **Methods:**

  - ##### `def validate(self, plan_content, model)`

    > Validates a plan against a given CSDC model.
    >
    > Args:
    >     plan_content: The string content of the plan.
    >     model: The CSDC model to validate against ('A' or 'B').
    >
    > Returns:
    >     A tuple containing a boolean indicating validity and a string with an error message.


### `/app/tooling/lfi_ill_halting_decider.py`

A tool for analyzing the termination of LFI-ILL programs.

This script takes an LFI-ILL file, interprets it in a paraconsistent logic
environment, and reports on its halting status. It does this by setting up
a paradoxical initial state and observing how the program resolves it.


**Public Functions:**


- #### `def main()`



**Public Classes:**


- #### `class LfiIllHaltingDecider`


  **Methods:**

  - ##### `def __init__(self, lfi_ill_file)`

  - ##### `def analyze(self)`

    > Analyzes the LFI ILL program for termination.


### `/app/tooling/lfi_udc_model.py`

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


**Public Classes:**


- #### `class LFIExecutor`

  > A paraconsistent interpreter for UDC plans.
  >
  > It models the state of the UDC machine not with concrete values, but with
  > ParaconsistentState objects. This allows it to explore the consequences
  > of contradictory assumptions.


  **Methods:**

  - ##### `def __init__(self, instructions, labels)`

  - ##### `def get_register(self, name)`

    > Gets a register's state, initializing if not present.

  - ##### `def run_step(self)`

    > Executes a single instruction step.


- #### `class LFIInstruction`

  > A wrapper for UDC instructions to be used in the LFI Executor.


  **Methods:**

  - ##### `def __init__(self, opcode, args)`

  - ##### `def __repr__(self)`

  - ##### `def execute(self, executor)`

    > Executes the instruction on the given LFI executor state.


- #### `class ParaconsistentHaltingDecider`

  > Analyzes a UDC plan using the LFI Executor to determine its
  > paraconsistent halting status.


  **Methods:**

  - ##### `def __init__(self, plan_path, max_steps=100)`

  - ##### `def analyze(self)`

    > Runs the analysis and returns the final paraconsistent halting state.


- #### `class ParaconsistentState`

  > A variable whose truth value is modeled paraconsistently.
  > It can be true, false, both, or neither.


  **Methods:**

  - ##### `def __init__(self, value=...)`

  - ##### `def __repr__(self)`

  - ##### `def is_consistent(self)`

    > A state is consistent if it's not BOTH.

  - ##### `def is_false(self)`

    > Classical check: Is False in the value set?

  - ##### `def is_true(self)`

    > Classical check: Is True in the value set?


- #### `class ParaconsistentTruth`

  > Represents the four truth values in a first-degree entailment logic (FDE),
  > which is a common foundation for Logics of Formal Inconsistency.


  **Methods:**

  - ##### `def __str__(self)`


### `/app/tooling/log_failure.py`

A dedicated script to log a catastrophic failure event to the main activity log.

This tool is designed to be invoked in the rare case of a severe, unrecoverable
error that violates a core protocol. Its primary purpose is to ensure that such
a critical event is formally and structurally documented in the standard agent
activity log (`logs/activity.log.jsonl`), even if the main agent loop has
crashed or been terminated.

The script is pre-configured to log a `SYSTEM_FAILURE` event, specifically
attributing it to the "Unauthorized use of the `reset_all` tool." This creates a
permanent, machine-readable record of the failure, which is essential for
post-mortem analysis, debugging, and the development of future safeguards.

By using the standard `Logger` class, it ensures that the failure log entry
conforms to the established `LOGGING_SCHEMA.md`, making it processable by
auditing and analysis tools.


**Public Functions:**


- #### `def log_catastrophic_failure()`

  > Logs the catastrophic failure event.


### `/app/tooling/master_agents_md_generator.py`

Generates the master AGENTS.md file by synthesizing information from the
compiled system documentation, the integrated knowledge core, and the build
configuration.

This script is the final step in the build process and is responsible for
creating the primary entry point for any AI agent interacting with this
repository. It addresses the problem of "contextual blindness" by ensuring
the AGENTS.md file is not just a static list of commands, but a dynamic,
context-rich overview of the entire project's architecture, knowledge, and
capabilities.


**Public Functions:**


- #### `def main()`


- #### `def summarize_build_commands(config_path)`

  > Reads the build configuration and creates a summary of available commands.


- #### `def summarize_knowledge_core(knowledge_path)`

  > Reads the integrated knowledge graph and creates a high-level summary.


- #### `def summarize_system_documentation(doc_path)`

  > Reads the full system documentation and creates a high-level summary.


### `/app/tooling/master_control.py`

The master orchestrator for the agent's lifecycle, implementing the Context-Free Development Cycle (CFDC).

This script, master_control.py, is the heart of the agent's operational loop.
It implements the CFDC, a hierarchical planning and execution model based on a
Pushdown Automaton. This allows the agent to execute complex tasks by calling
plans as sub-routines.

Core Responsibilities:
- **Hierarchical Plan Execution:** Manages a plan execution stack to enable
  plans to call other plans via the `call_plan` directive. This allows for
  modular, reusable, and complex task decomposition. A maximum recursion depth
  is enforced to guarantee decidability.
- **Plan Validation:** Contains the in-memory plan validator. Before execution,
  it parses a plan and simulates its execution against a Finite State Machine
  (FSM) to ensure it complies with the agent's operational protocols.
- **"Registry-First" Plan Resolution:** When resolving a `call_plan` directive,
  it first attempts to look up the plan by its logical name in the
  `knowledge_core/plan_registry.json`. If not found, it falls back to treating
  the argument as a direct file path.
- **FSM-Governed Lifecycle:** The entire workflow, from orientation to
  finalization, is governed by a strict FSM definition (e.g., `tooling/fsm.json`)
  to ensure predictable and auditable behavior.

This module is designed as a library to be controlled by an external shell
(e.g., `agent_shell.py`), making its interaction purely programmatic.


**Public Classes:**


- #### `class MasterControlGraph`

  > A Finite State Machine (FSM) that enforces the agent's protocol.
  > This graph reads a state definition and orchestrates the agent's workflow,
  > ensuring that all protocol steps are followed in the correct order.


  **Methods:**

  - ##### `def __init__(self, fsm_path='tooling/fsm.json')`

  - ##### `def do_awaiting_result(self, agent_state, logger)`

    > Checks for the result of the background research process.

  - ##### `def do_debugging(self, agent_state, logger)`

    > Handles the debugging state.

  - ##### `def do_execution(self, agent_state, step_result, logger)`

    > Processes the result of a step and advances the execution state.

  - ##### `def do_finalizing(self, agent_state, analysis_content, logger)`

    > Handles the finalization of the task, guiding the agent through
    > the structured post-mortem process.

  - ##### `def do_generating_code(self, agent_state, logger)`

    > Handles the code generation state.

  - ##### `def do_orientation(self, agent_state, logger, tools)`

    > Executes orientation, including analyzing the last post-mortem and scanning the filesystem.

  - ##### `def do_planning(self, agent_state, plan_content, logger)`

    > Validates a given plan, parses it, and initializes the plan stack.

  - ##### `def do_researching(self, agent_state, logger)`

    > Launches the background research process.

  - ##### `def do_running_tests(self, agent_state, logger)`

    > Handles the test execution state.

  - ##### `def get_current_step(self, agent_state)`

    > Returns the current command to be executed by the agent, or None if execution is complete.

  - ##### `def get_trigger(self, source_state, dest_state)`

    > Finds a trigger in the FSM definition for a transition from a source
    > to a destination state. This is a helper to avoid hardcoding trigger
    > strings in the state handlers.

  - ##### `def validate_plan_for_model(self, plan_content, model)`

    > Validates a plan against a specific CSDC model using the LBAValidator.


### `/app/tooling/master_control_cli.py`

The official command-line interface for the agent's master control loop.

This script is now a lightweight wrapper that passes control to the new,
API-driven `agent_shell.py`. It preserves the command-line interface while
decoupling the entry point from the FSM implementation.


**Public Functions:**


- #### `def main()`

  > The main entry point for the agent.
  >
  > This script parses the task description and invokes the agent shell.


### `/app/tooling/message_user.py`

A dummy tool that prints its arguments to simulate the message_user tool.

This script is a simple command-line utility that takes a string as an
argument and prints it to standard output, prefixed with "[Message User]:".
Its purpose is to serve as a stand-in or mock for the actual `message_user`
tool in testing environments where the full agent framework is not required.

This allows for the testing of scripts or workflows that call the
`message_user` tool without needing to invoke the entire agent messaging
subsystem.


**Public Functions:**


- #### `def main()`

  > Prints the first command-line argument to simulate a user message.


### `/app/tooling/migrate_protocols.py`

_No module-level docstring found._


**Public Functions:**


- #### `def migrate_protocols(source_dir)`

  > Parses an old AGENTS.md file and migrates its content to .protocol.json
  > and .protocol.md files.


### `/app/tooling/pda_parser.py`

A parser for pLLLU (paraconsistent Linear Logic with Undeterminedness) formulas.

This script uses the PLY (Python Lex-Yacc) library to define a lexer and a
parser for a simple, string-based representation of pLLLU formulas. It can
handle basic atomic formulas, unary operators (like negation and consistency),
and binary operators (like implication and conjunction).

The main function `parse_formula` takes a string and returns a simple AST
(Abstract Syntax Tree) represented as nested tuples.


**Public Functions:**


- #### `def AtomNode(name)`


- #### `def BinaryOpNode(op, left, right)`


- #### `def UnaryOpNode(op, child)`


- #### `def p_error(p)`


- #### `def p_formula_atom(p)`

  > formula : ATOM


- #### `def p_formula_binary(p)`

  > formula : formula IMPLIES formula
  >         | formula WITH formula
  >         | formula PLUS formula


- #### `def p_formula_group(p)`

  > formula : LPAREN formula RPAREN


- #### `def p_formula_unary(p)`

  > formula : NOT formula
  >         | BANG formula
  >         | CONSISTENCY formula
  >         | SECTION formula
  >         | WHYNOT formula


- #### `def parse_formula(formula_string)`

  > Parses a pLLLU formula string into an AST.


- #### `def t_ATOM(t)`

  > [A-Z][A-Z0-9]*


- #### `def t_error(t)`


- #### `def t_newline(t)`

  > \n+


### `/app/tooling/plan_executor.py`

A simple plan executor for simulating agent behavior.

This script reads a plan file, parses it, and executes the commands in a
simplified, simulated environment. It supports a limited set of tools
(`message_user` and `run_in_bash_session`) to provide a basic demonstration
of how an agent would execute a plan.


**Public Functions:**


- #### `def execute_plan(filepath)`

  > Executes a plan file, simulating the agent's execution loop.
  >
  > Args:
  >     filepath: The path to the plan file.


- #### `def main()`

  > Main function to run the plan executor from the command line.


### `/app/tooling/plan_generator.py`

_No module-level docstring found._


**Public Functions:**


- #### `def find_agent_that_produces(resource_name)`

  > Finds an agent in the repository that produces the given resource.


- #### `def generate_plan(goal)`

  > Generates a plan to accomplish the given goal using backward-chaining.


### `/app/tooling/plan_manager.py`

Provides a command-line interface for managing the agent's Plan Registry.

This script is the administrative tool for the Plan Registry, a key component
of the Context-Free Development Cycle (CFDC) that enables hierarchical and
modular planning. The registry, located at `knowledge_core/plan_registry.json`,
maps human-readable, logical names to the file paths of specific plans. This
decouples the `call_plan` directive from hardcoded file paths, making plans
more reusable and the system more robust.

This CLI provides three essential functions:
- **register**: Associates a new logical name with a plan file path, adding it
  to the central registry.
- **deregister**: Removes an existing logical name and its associated path from
  the registry.
- **list**: Displays all current name-to-path mappings in the registry.

By providing a simple, standardized interface for managing this library of
reusable plans, this tool improves the agent's ability to compose complex
workflows from smaller, validated sub-plans.


**Public Functions:**


- #### `def deregister_plan(name)`

  > Removes a plan from the registry by its logical name.


- #### `def get_registry()`

  > Loads the plan registry from its JSON file.


- #### `def list_plans()`

  > Lists all currently registered plans.


- #### `def main()`

  > Main function to run the plan management CLI.


- #### `def register_plan(name, path)`

  > Registers a new plan by mapping a logical name to a file path.


- #### `def save_registry(registry_data)`

  > Saves the given data to the plan registry JSON file.


### `/app/tooling/plan_parser.py`

Parses a plan file into a structured list of commands.

This module provides the `parse_plan` function and the `Command` dataclass,
which are central to the agent's ability to understand and execute plans.
The parser correctly handles multi-line arguments and ignores comments,
allowing for robust and readable plan files.


**Public Functions:**


- #### `def parse_plan(plan_content)`

  > Parses the raw text of a plan into a list of Command objects.
  > This parser correctly handles multi-line arguments, comments, and the '---' separator.



**Public Classes:**


- #### `class Command`

  > Represents a single, parsed command from a plan.
  > This structure correctly handles multi-line arguments for tools.


### `/app/tooling/plllu_interpreter.py`

A resource-sensitive, four-valued interpreter for pLLLU formulas.

This script implements an interpreter for the pLLLU language. It operates on
an AST generated by the `pda_parser.py` script. The interpreter is designed
to be resource-sensitive, meaning that each atomic formula in the initial
context must be consumed exactly once during the evaluation of the proof.

The logic is four-valued, supporting TRUE, FALSE, BOTH, and NEITHER, allowing
it to reason about paraconsistent and paracomplete states.

The core of the interpreter is the `FourValuedInterpreter` class, which
recursively walks the AST, consuming resources from a context (a Counter of
available atoms) and returning the resulting logical value.


**Public Functions:**


- #### `def create_context_from_string(s)`

  > Helper to create a context from a string like 'A:T, B:B'.
  > The interpreter now expects the context to be a dictionary mapping
  > the unique atom tuple (name, id) to its LogicValue.


- #### `def patch_atom_values(node, context_values)`

  > Recursively patches the AST to replace atom names with (value, id) tuples.
  > This is a hack for testing, as the parser doesn't know about logic values.



**Public Classes:**


- #### `class FourValuedInterpreter`

  > Interprets a pLLLU AST using a four-valued logic and a resource-passing model.


  **Methods:**

  - ##### `def interpret(self, ast_node, initial_context)`

    > Main entry point for interpreting an AST.
    > The initial context is a Counter of atoms available.


- #### `class InterpretationError`

  > Custom exception for errors during interpretation.


- #### `class LogicValue`


### `/app/tooling/plllu_runner.py`

A command-line runner for pLLLU files.

This script provides an entry point for executing `.plllu` files. It
integrates the pLLLU lexer, parser, and interpreter to execute the logic
defined in a given pLLLU source file and print the result.


**Public Functions:**


- #### `def main()`

  > This tool provides a command-line interface for running .plllu files.
  > It integrates the pLLLU lexer, parser, and interpreter to execute
  > the logic defined in a given pLLLU source file.


### `/app/tooling/pre_submit_check.py`

_No module-level docstring found._


**Public Functions:**


- #### `def main()`

  > Main function to run pre-submission checks.


- #### `def run_command(command, description)`

  > Runs a command and exits if it fails.


### `/app/tooling/protocol_manager.py`

A command-line tool for managing agent protocols.

This script provides a set of commands for creating, testing, and versioning
agent protocols. It is designed to be used by developers to manage the
protocol lifecycle.


**Public Functions:**


- #### `def create_protocol(name, directory)`

  > Creates a new protocol from a template.


- #### `def main()`

  > Main function for the protocol manager.


- #### `def run_tests()`

  > Runs the protocol tests.


- #### `def update_version(protocol_id, new_version)`

  > Updates the version of a protocol.


### `/app/tooling/protocol_oracle.py`

_No module-level docstring found._


**Public Functions:**


- #### `def get_applicable_protocols(graph, context)`

  > Queries the graph to find protocols that are applicable to the given context.
  > This function dynamically loads and executes the `is_applicable` function
  > from the Python protocol files.


- #### `def get_rules_for_protocols(graph, protocol_uris)`

  > Retrieves all rules associated with the given list of protocol URIs.


- #### `def main()`


### `/app/tooling/protocol_updater.py`

A command-line tool for programmatically updating protocol source files.

This script provides the mechanism for the agent to perform self-correction
by modifying its own governing protocols based on structured, actionable
lessons. It is a key component of the Protocol-Driven Self-Correction (PDSC)
workflow.

The tool operates on the .protocol.json files located in the `protocols/`
directory, performing targeted updates based on command-line arguments.


**Public Functions:**


- #### `def add_tool_to_protocol(protocol_id, tool_name, protocols_dir)`

  > Adds a tool to the 'associated_tools' list of a specified protocol.


- #### `def find_protocol_file(protocol_id, protocols_dir)`

  > Recursively finds the protocol file path corresponding to a given protocol_id.


- #### `def main()`

  > Main function to parse arguments and call the appropriate handler.


- #### `def update_rule_in_protocol(protocol_id, rule_id, new_description, protocols_dir)`

  > Updates the description of a specific rule within a protocol.


### `/app/tooling/refactor.py`

A tool for performing automated symbol renaming in Python code.

This script provides a command-line interface to find a specific symbol
(a function or a class) in a given Python file and rename it, along with all of
its textual references throughout the entire repository. This provides a safe
and automated way to perform a common refactoring task, reducing the risk of
manual errors.


**Public Functions:**


- #### `def find_references(symbol_name, search_path)`

  > Finds all files in a directory that reference a given symbol.


- #### `def find_symbol_definition(filepath, symbol_name)`

  > Finds the definition of a symbol in a Python file.


- #### `def main()`


### `/app/tooling/reliable_ls.py`

A tool for reliably listing files and directories.

This script provides a consistent, sorted, and recursive listing of files and
directories, excluding the `.git` directory. It is intended to be a more
reliable alternative to the standard `ls` command for agent use cases.


**Public Functions:**


- #### `def main()`

  > Main function to run the reliable_ls tool from the command line.


- #### `def reliable_ls(start_path='.')`

  > Recursively lists all directories and files under the start_path.
  >
  > Args:
  >     start_path: The directory to start the traversal from.


### `/app/tooling/reorientation_manager.py`

Re-orientation Manager

This script is the core of the automated re-orientation process. It is
designed to be triggered by the build system whenever the agent's core
protocols (`AGENTS.md`) are re-compiled.

The manager performs the following key functions:
1.  **Diff Analysis:** It compares the old version of AGENTS.md with the new
    version to identify new protocols, tools, or other key concepts that have
    been introduced.
2.  **Temporal Orientation (Shallow Research):** For each new concept, it
    invokes the `temporal_orienter.py` tool to fetch a high-level summary from
    an external knowledge base like DBpedia. This ensures the agent has a
    baseline understanding of new terms.
3.  **Knowledge Storage:** The summaries from the temporal orientation are
    stored in a structured JSON file (`knowledge_core/temporal_orientations.json`),
    creating a persistent, queryable knowledge artifact.
4.  **Deep Research Trigger:** It analyzes the nature of the changes. If a
    change is deemed significant (e.g., the addition of a new core
    architectural protocol), it programmatically triggers a formal L4 Deep
    Research Cycle by creating a `deep_research_required.json` file.

This automated workflow ensures that the agent never operates with an outdated
understanding of its own protocols. It closes the loop between protocol
modification and the agent's self-awareness, making the system more robust,
adaptive, and reliable.


**Public Functions:**


- #### `def check_for_deep_research_trigger(new_concepts)`

  > Checks if any of the new concepts should trigger a deep research cycle.


- #### `def main()`


- #### `def parse_concepts_from_agents_md(content)`

  > Parses an AGENTS.md file to extract a set of key concepts.
  > This version uses a simple regex to find protocol IDs and tool names.


- #### `def run_temporal_orientation(concept)`

  > Runs the temporal_orienter.py tool for a given concept.


- #### `def update_temporal_orientations(new_orientations)`

  > Updates the temporal orientations knowledge base.


### `/app/tooling/research.py`

This module contains the logic for executing research tasks based on a set of
constraints. It acts as a dispatcher, calling the appropriate tool (e.g.,
read_file, google_search) based on the specified target and scope.


**Public Functions:**


- #### `def execute_research_protocol(constraints)`

  > Executes a research task based on a provided constraints dictionary.
  >
  > Args:
  >     constraints (dict): A dictionary specifying the research target,
  >                         scope, and other parameters.
  >
  > Returns:
  >     str: The result of the research action, or an error message.


### `/app/tooling/research_planner.py`

This module is responsible for generating a formal, FSM-compliant research plan
for a given topic. The output is a string that can be executed by the agent's
master controller.


**Public Functions:**


- #### `def plan_deep_research(topic, research_id)`

  > Generates a multi-step, FSM-compliant plan for conducting deep research
  > using the official project templates.
  >
  > Args:
  >     topic (str): The research topic.
  >     research_id (str): A unique ID for this research task.
  >
  > Returns:
  >     str: A string containing the executable plan.


### `/app/tooling/self_correction_orchestrator.py`

Orchestrates the Protocol-Driven Self-Correction (PDSC) workflow.

This script is the engine of the automated feedback loop. It reads structured,
actionable lessons from `knowledge_core/lessons.jsonl` and uses the
`protocol_updater.py` tool to apply them to the source protocol files.


**Public Functions:**


- #### `def load_lessons()`

  > Loads all lessons from the JSONL file.


- #### `def main()`

  > Main function to run the self-correction workflow.


- #### `def process_lessons(lessons, protocols_dir)`

  > Processes all pending lessons, applies them, and updates their status.
  > Returns True if any changes were made, False otherwise.


- #### `def run_command(command)`

  > Runs a command and returns True on success, False on failure.


- #### `def save_lessons(lessons)`

  > Saves a list of lessons back to the JSONL file, overwriting it.


### `/app/tooling/self_improvement_cli.py`

A command-line tool for initiating a new self-improvement proposal.

This script is the entry point for the Self-Improvement Protocol (SIP). It
automates the boilerplate process of creating a new proposal, ensuring that all
proposals are structured correctly and stored in a consistent location.

When executed, this tool will:
1.  Create a new, timestamped directory within the `proposals/` directory to
    house the new proposal.
2.  Generate a `proposal.md` file within that new directory.
3.  Populate the `proposal.md` with a standard template that includes all the
    required sections as defined in the Self-Improvement Protocol (rule sip-002).
4.  Print the path to the newly created proposal file, so the agent can
    immediately begin editing it.


**Public Functions:**


- #### `def create_proposal()`

  > Creates a new, structured proposal for self-improvement.


- #### `def main()`

  > Main function to run the self-improvement proposal generator.


### `/app/tooling/state.py`

Defines the core data structures for managing the agent's state.

This module provides the `AgentState` and `PlanContext` dataclasses, which are
fundamental to the operation of the Context-Free Development Cycle (CFDC). These
structures allow the `master_control.py` orchestrator to maintain a complete,
snapshot-able representation of the agent's progress through a task.

- `AgentState`: The primary container for all information related to the current
  task, including the plan execution stack, message history, and error states.
- `PlanContext`: A specific structure that holds the state of a single plan
  file, including its content and the current execution step. This is the
  element that gets pushed onto the `plan_stack` in `AgentState`.

Together, these classes enable the hierarchical, stack-based planning and
execution that is the hallmark of the CFDC.


**Public Classes:**


- #### `class AgentState`

  > Represents the complete, serializable state of the agent's workflow.
  >
  > This dataclass acts as a central container for all information related to the
  > agent's current task. It is designed to be passed between the different states
  > of the `MasterControlGraph` FSM, ensuring that context is maintained
  > throughout the lifecycle of a task.
  >
  > Attributes:
  >     task: A string describing the overall objective.
  >     plan_path: The file path to the root plan for the current task.
  >     plan_stack: A list of `PlanContext` objects, forming the execution
  >         stack for the CFDC. The plan at the top of the stack is the one
  >         currently being executed.
  >     messages: A history of messages, typically for interaction with an LLM.
  >     orientation_complete: A flag indicating if the initial orientation
  >         phase has been successfully completed.
  >     vm_capability_report: A string summarizing the results of the
  >         environmental probe.
  >     research_findings: A dictionary to store the results of research tasks.
  >     draft_postmortem_path: The file path to the draft post-mortem report
  >         generated during the AWAITING_ANALYSIS state.
  >     final_report: A string containing a summary of the final, completed
  >         post-mortem report.
  >     error: An optional string that holds an error message if the FSM
  >         enters an error state, providing a clear reason for the failure.


  **Methods:**

  - ##### `def to_json(self)`


- #### `class PlanContext`

  > Represents the execution context of a single plan file within the plan stack.
  >
  > This class holds the state of a specific plan being executed, including its
  > file path, its content (as a list of parsed Command objects), and a pointer
  > to the current step being executed.


### `/app/tooling/symbol_map_generator.py`

Generates a code symbol map for the repository to aid in contextual understanding.

This script creates a `symbols.json` file in the `knowledge_core` directory,
which acts as a high-level index of the codebase. This map contains information
about key programming constructs like classes and functions, including their
name, location (file path and line number), and language.

The script employs a two-tiered approach for symbol generation:
1.  **Universal Ctags (Preferred):** It first checks for the presence of the
    `ctags` command-line tool. If available, it uses `ctags` to perform a
    comprehensive, multi-language scan of the repository. This is the most
    robust and accurate method.
2.  **AST Fallback (Python-only):** If `ctags` is not found, the script falls
    back to using Python's built-in Abstract Syntax Tree (`ast`) module. This
    method parses all `.py` files and extracts symbol information for Python
    code. While less comprehensive than `ctags`, it ensures that a baseline
    symbol map is always available.

The resulting `symbols.json` artifact is a critical input for the agent's
orientation and planning phases, allowing it to quickly locate relevant code
and understand the structure of the repository without having to read every file.


**Public Functions:**


- #### `def generate_symbols_with_ast(root_dir='.')`

  > Fallback to generate a symbol map for Python files using the AST module.


- #### `def generate_symbols_with_ctags(root_dir='.')`

  > Generates a symbol map using Universal Ctags.


- #### `def has_ctags()`

  > Check if Universal Ctags is installed and available in the PATH.


- #### `def main()`

  > Main function to generate and save the symbol map.


### `/app/tooling/udc_orchestrator.py`

An orchestrator for executing Unrestricted Development Cycle (UDC) plans.

This script provides a sandboxed environment for running UDC plans, which are
low-level assembly-like programs that can perform Turing-complete computations.
The orchestrator acts as a virtual machine with a tape-based memory model,
registers, and a set of simple instructions.

To prevent non-termination and other resource-exhaustion issues, the
orchestrator imposes strict limits on the number of instructions executed,
the amount of memory used, and the total wall-clock time.


**Public Functions:**


- #### `def main()`



**Public Classes:**


- #### `class Instruction`


  **Methods:**

  - ##### `def __init__(self, opcode, args)`

  - ##### `def __repr__(self)`


- #### `class UDCOrchestrator`

  > Executes an Unrestricted Development Cycle (UDC) plan within a sandboxed
  > Turing Machine-like environment with strict resource limits.


  **Methods:**

  - ##### `def __init__(self, plan_path, max_instructions=10000, max_memory_cells=1000, max_time_s=5)`

  - ##### `def run(self)`

    > Parses and runs the UDC plan until it halts or a limit is exceeded.


### `/app/tooling/validate_tdd.py`

_No module-level docstring found._

---

## `/app/tooling/aal/` Directory

### `/app/tooling/aal/__init__.py`

_No module-level docstring found._

### `/app/tooling/aal/domain.py`

_No module-level docstring found._


**Public Classes:**


- #### `class Action`

  > Represents an action that can be performed by an agent.


- #### `class CausalLaw`

  > Represents a causal law of the form 'a causes f if p1, ..., pn'.


- #### `class Domain`

  > Represents a complete AAL domain description.


  **Methods:**

  - ##### `def __init__(self)`


- #### `class Fluent`

  > Represents a fluent (a proposition) in the domain.


### `/app/tooling/aal/interpreter.py`

_No module-level docstring found._


**Public Classes:**


- #### `class Interpreter`

  > The AAL interpreter, responsible for state transitions.


  **Methods:**

  - ##### `def get_next_state(self, current_state, action, domain)`

    > Calculates the next state based on the current state, an action, and the domain's causal laws.
    > A fluent is in the next state if there is a causal law 'a causes f if C' where a is the action
    > and C is a subset of the current state.


### `/app/tooling/aal/parser.py`

_No module-level docstring found._


**Public Functions:**


- #### `def parse_aal(aal_string)`

  > Parses an AAL string and returns a Domain object.


---

## `/app/tooling/agent_smith/` Directory

### `/app/tooling/agent_smith/__init__.py`

_No module-level docstring found._

### `/app/tooling/agent_smith/generate_and_test.py`

_No module-level docstring found._


**Public Functions:**


- #### `def apply_mutation(sandbox_path, mutation_target)`

  > Applies the specified mutation to the sandboxed sources.


- #### `def cleanup_sandbox(sandbox_path)`

  > Deletes the sandbox directory.


- #### `def compile_variant(sandbox_path, python_path_ext)`

  > Runs the hierarchical compiler inside the sandbox.


- #### `def copy_sources(root_dir, sandbox_path)`

  > Copies the necessary source files and compiler into the sandbox.


- #### `def create_sandbox(root_dir, sandbox_path)`

  > Creates a clean sandbox directory.


- #### `def get_repo_root()`

  > Gets the absolute path of the repository root.


- #### `def install_dependencies(sandbox_path)`

  > Installs dependencies from requirements.txt into the sandbox.


- #### `def log_step(message)`

  > Prints a formatted step message.


- #### `def main()`

  > Main function to orchestrate the generation and testing process.


- #### `def run_command(command, cwd)`

  > Runs a command in a subprocess and handles errors.


- #### `def verify_variant(variant_path, mutation_check_string)`

  > Performs a basic verification to check the variant was created correctly.


---

## `/app/tooling/custom_tools/` Directory

### `/app/tooling/custom_tools/analyze_data.py`

_No module-level docstring found._


**Public Functions:**


- #### `def main()`


### `/app/tooling/custom_tools/create_file.py`

_No module-level docstring found._


**Public Functions:**


- #### `def main()`


### `/app/tooling/custom_tools/fetch_data.py`

_No module-level docstring found._


**Public Functions:**


- #### `def main()`


### `/app/tooling/custom_tools/hello_world.py`

_No module-level docstring found._


**Public Functions:**


- #### `def hello_world(message)`

  > Prints a message to the console.


### `/app/tooling/custom_tools/read_file.py`

_No module-level docstring found._


**Public Functions:**


- #### `def main()`


---

## `/app/tooling/jules_agent/` Directory

### `/app/tooling/jules_agent/action_logger.py`

_No module-level docstring found._


**Public Functions:**


- #### `def get_agents_md_path(cwd)`

  > Finds the AGENTS.md file in the given directory.


- #### `def log_action(action_text, cwd)`

  > Logs an action to the AGENTS.md file.


### `/app/tooling/jules_agent/plan_manager.py`

_No module-level docstring found._


**Public Functions:**


- #### `def get_agents_md_path(cwd)`

  > Finds the AGENTS.md file in the given directory.


- #### `def inject_plan(plan_text, cwd)`

  > Injects or updates the plan in the AGENTS.md file.


### `/app/tooling/jules_agent/plan_runner.py`

A self-executing plan runner for Jules, the AI agent.

This script reads a plan file in a specific format, executes the commands,
verifies their success, and handles failures.


**Public Functions:**


- #### `def execute_command(command, cwd)`

  > Executes a single command and returns True on success, False on failure.


- #### `def main()`

  > Main function to run the plan runner from the command line.


- #### `def message_user(message)`

  > Simulates sending a message to the user.


- #### `def parse_executable_plan(plan_content)`

  > Parses the raw text of a plan into a list of ExecutableCommand objects.


- #### `def run_in_bash_session(command)`

  > Simulates running a command in a bash session.


- #### `def run_plan(plan_content, cwd)`

  > Parses and executes a plan.



**Public Classes:**


- #### `class ExecutableCommand`

  > Represents a single, parsed command from a self-executing plan.


---

## `/app/utils/` Directory

### `/app/utils/__init__.py`

_No module-level docstring found._

### `/app/utils/file_system_utils.py`

This module provides a centralized and standardized interface for all file
system operations within the agent's environment. It aims to address issues of
inconsistent path handling, duplicated file discovery logic, and ad-hoc
filtering by providing a single, reliable implementation for these common tasks.

Core Features:
- **Standardized Path Construction:** All path manipulations are handled using
  `os.path.join` to ensure cross-platform compatibility.
- **Centralized File Discovery:** A single function for finding files based on
  patterns, with built-in support for a centralized ignore mechanism.
- **Robust Error Handling:** Functions are designed to gracefully handle common
  file system errors, such as permission issues or broken links.
- **Centralized Ignore Mechanism:** File and directory filtering is managed via
  a `.julesignore` file in the repository root, providing a single source of
  truth for exclusion patterns.


**Public Functions:**


- #### `def find_files(pattern, base_dir=ROOT_DIR, recursive=True)`

  > Finds all files matching a given pattern, respecting the .julesignore file.
  > Can perform both recursive and non-recursive searches.


- #### `def find_protocol_dirs(root_dir)`

  > Finds all directories within the root_dir that contain at least one
  > `.protocol.json` or `.protocol.md` file, indicating they are protocol modules.


- #### `def get_ignore_patterns(base_dir)`

  > Loads ignore patterns from the .julesignore file in the specified base directory.
  > Returns two sets of patterns: one for directories and one for files.


- #### `def get_protocol_dir_name(dir_path)`

  > Returns a human-readable name for a protocol directory.
  > If it's the root protocols directory, it returns 'root'.
  > Otherwise, it returns the directory's base name.


### `/app/utils/logger.py`

Provides a standardized, schema-validated logger for producing structured JSONL logs.

This module contains the `Logger` class, which is responsible for creating all
entries in the `logs/activity.log.jsonl` file. This is a critical component for
maintaining an auditable, machine-readable record of the agent's actions.

The logger enforces a strict structure on all log entries by validating them
against a formal JSON schema, which is extracted from the `LOGGING_SCHEMA.md`
document. This ensures that every log entry, regardless of its source, is
consistent and contains the required fields.

Key features of the `Logger` class:
- **Schema Validation:** Each log entry is validated against the official
  project schema before being written to disk, preventing data corruption.
- **Structured Data:** Logs are written in JSONL format, where each line is a
  valid JSON object, making them easy to parse and query.
- **Session Management:** It automatically assigns a unique `session_id` to
  all logs generated during its lifecycle, allowing actions to be traced back
  to a specific run.
- **Automatic Timestamps:** It injects a UTC timestamp into every log entry,
  providing a precise timeline of events.

This centralized logger is the sole mechanism by which the agent should record
its activities, ensuring a single source of truth for all post-mortem analysis
and self-improvement activities.


**Public Classes:**


- #### `class Logger`

  > A class to handle structured logging to a JSONL file, validated against a schema.


  **Methods:**

  - ##### `def __init__(self, schema_path='LOGGING_SCHEMA.md', log_path='logs/activity.log.jsonl')`

    > Initializes the Logger, loading the schema and setting up the session.
    >
    > Args:
    >     schema_path (str): The path to the Markdown file containing the logging schema.
    >     log_path (str): The path to the log file to be written.

  - ##### `def get_logs(self)`

    > Retrieves all log entries for the current session.
    >
    > Returns:
    >     list: A list of log entries for the current session.

  - ##### `def log(self, phase, task_id, plan_step, action_type, action_details, outcome_status, outcome_message='', error_details=None, evidence='', context=None)`

    > Constructs, validates, and writes a log entry.
    >
    > Args:
    >     phase (str): The current protocol phase (e.g., "Phase 7").
    >     task_id (str): The ID of the current task.
    >     plan_step (int): The current plan step number.
    >     action_type (str): The type of action (e.g., "TOOL_EXEC").
    >     action_details (dict): Details specific to the action.
    >     outcome_status (str): The outcome of the action ("SUCCESS", "FAILURE").
    >     outcome_message (str, optional): A message describing the outcome. Defaults to "".
    >     error_details (dict, optional): Structured error info if the outcome is a failure. Defaults to None.
    >     evidence (str, optional): Citation for the action. Defaults to "".
    >     context (dict, optional): The agent's internal context. Defaults to None.
    >
    > Raises:
    >     ValidationError: If the generated log entry does not conform to the schema.


---

## `/app/utils/gemini_api/` Directory

### `/app/utils/gemini_api/client.py`

_No module-level docstring found._


**Public Classes:**


- #### `class GeminiApiClient`

  > A client for interacting with the Gemini API.


  **Methods:**

  - ##### `def __init__(self, api_key=None)`

    > Initializes the Gemini API client.
    > Args:
    >     api_key: The API key for the Gemini API. If not provided, it will be
    >         read from the GEMINI_API_KEY environment variable.

  - ##### `def generate_text(self, prompt)`

    > Generates text using the Gemini API.
    > Args:
    >     prompt: The prompt to use for text generation.
    > Returns:
    >     The generated text.

  - ##### `def process_document(self, document_path, prompt='Extract the text from this document.')`

    > Processes a document using the Gemini API.
    > Args:
    >     document_path: The path to the document to process.
    >     prompt: The prompt to use for document processing.
    > Returns:
    >     The processed document content.
