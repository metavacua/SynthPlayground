# Language Classification Report

## 1. Definition of a "Program"

For the purposes of this analysis, a "program" is defined as a self-contained, executable unit of logic that can be classified according to the Chomsky hierarchy. This includes:

- **Language Implementations:** Interpreters, parsers, and lexers for any domain-specific language (DSL) or programming language defined within the repository.
- **Executable Scripts and Core Tooling:** Standalone scripts and tools that perform specific tasks, such as build automation, testing, or data processing.
- **Finite State Machines (FSMs):** Files that explicitly define a Finite State Machine, which are inherently regular programs.

## 2. Program Classifications

### 2.1. Regular Programs

- **Finite Development Cycle (FDC) FSM:**
    - **Files:** `tooling/fdc_fsm.json`
    - **Justification:** This file defines a Finite State Machine, which is a model of computation for regular languages. The FSM has a finite number of states and transitions, and it accepts or rejects strings based on a predefined set of rules.
    - **DBpedia:** [https://dbpedia.org/page/Finite-state_machine](https://dbpedia.org/page/Finite-state_machine)

- **Research FSM:**
    - **Files:** `tooling/research_fsm.json`
    - **Justification:** Similar to the FDC FSM, this file defines a Finite State Machine for the research process.
    - **DBpedia:** [https://dbpedia.org/page/Finite-state_machine](https://dbpedia.org/page/Finite-state_machine)

### 2.2. Context-Free Programs

- **Aura Language:**
    - **Files:** `aura_lang/`
    - **Justification:** The Aura language supports nested structures, which are characteristic of context-free languages. The language is parsed by a Pratt parser, which is a top-down operator-precedence parser, a common technique for parsing context-free grammars.
    - **Curry-Howard Correspondence:** The type system of the Aura language is simple and corresponds to a propositional logic.
    - **DBpedia:** [https://dbpedia.org/page/Context-free_grammar](https://dbpedia.org/page/Context-free_grammar)

- **LFI ILL Language:**
    - **Files:** `lfi_ill/`
    - **Justification:** The LFI ILL language is defined by a BNF grammar, a formal notation for describing context-free grammars.
    - **Curry-Howard Correspondence:** The LFI ILL language is a linear logic, which corresponds to a resource-sensitive lambda calculus.
    - **DBpedia:** [https://dbpedia.org/page/Linear_logic](https://dbpedia.org/page/Linear_logic)

- **AAL (Agent Abstraction Language):**
    - **Files:** `tooling/aal/`
    - **Justification:** The AAL language is designed to represent agent interactions, which can involve nested and recursive structures. This is a characteristic of context-free languages.
    - **Curry-Howard Correspondence:** The AAL language corresponds to a simple action logic.
    - **DBpedia:** [https://dbpedia.org/page/Action_logic](https://dbpedia.org/page/Action_logic)

- **pLLLU Language:**
    - **Files:** `tooling/plllu_interpreter.py`
    - **Justification:** The pLLLU language is a planning and automation language that supports nested and recursive structures, which are characteristic of context-free languages.
    - **Curry-Howard Correspondence:** The pLLLU language is a paraconsistent linear logic, which corresponds to a resource-sensitive lambda calculus that can handle contradictions.
    - **DBpedia:** [https://dbpedia.org/page/Paraconsistent_logic](https://dbpedia.org/page/Paraconsistent_logic)

### 2.3. Context-Sensitive Programs

- **HDL Prover:**
    - **Files:** `tooling/hdl_prover.py`
    - **Justification:** The HDL prover interacts with an external Lisp-based prover and its behavior is dependent on the state of the external process. This makes it context-sensitive.
    - **DBpedia:** [https://dbpedia.org/page/Context-sensitive_grammar](https://dbpedia.org/page/Context-sensitive_grammar)

- **Python Orchestration Scripts:**
    - **Files:** `tooling/`
    - **Justification:** The Python scripts in the `tooling/` directory are context-sensitive because their behavior is dependent on runtime conditions, such as the state of the file system, environment variables, and the outputs of other programs.
    - **DBpedia:** [https://dbpedia.org/page/Context-sensitive_grammar](https://dbpedia.org/page/Context-sensitive_grammar)

- **Gemini App Canvas Agent:**
    - **Files:** `GeminiAppCanvasAgent.jsx`
    - **Justification:** This is a React application that interacts with the user, the file system (via IndexedDB), and external services (the Gemini API).
    - **DBpedia:** [https://dbpedia.org/page/Context-sensitive_grammar](https://dbpedia.org/page/Context-sensitive_grammar)
