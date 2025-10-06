# P-Lang: A Minimalist Paraconsistent Language Specification (v0.1)

## 1. Introduction

P-Lang is a minimalist programming language designed to handle constructive contradictions as a first-class feature. It is a strict superset of a small subset of Python, extended with specific constructs for representing and resolving paraconsistent states. Its formal semantics are based on Belnap's four-valued logic.

## 2. Core Logic: Four-Valued Semantics

P-Lang is built upon the four truth values defined by Nuel Belnap:

-   **True:** A standard, classical true value. In P-Lang, this is any variable assigned a single, unambiguous value.
-   **False:** A standard, classical false value.
-   **Both (Dialetheia):** A state representing a contradiction, where a variable holds two or more mutually exclusive, self-consistent values simultaneously. This is the core paraconsistent state.
-   **Neither (Null):** A state representing a lack of information.

## 3. Syntax and Semantics

### 3.1. Python Subset

P-Lang incorporates a safe subset of Python, including:
-   Variable assignments (`x = 10`)
-   Function definitions and calls (`def my_func(): ...`)
-   Basic control flow (`if/else`)
-   Standard data types (strings, integers, lists, dictionaries)

### 3.2. The `dialetheia` Block

This is the core construct for representing the **Both** state.

**Syntax:**
```plang
dialetheia <variable_name>:
    "<stance_A_name>": <value_A>,
    "<stance_B_name>": <value_B>,
    # ... more stances and values
```

**Semantics:**
-   The `dialetheia` block declares that `<variable_name>` exists in a paraconsistent state.
-   It does not assign a value to the variable directly. Instead, it populates a "possibility space" for it.
-   Each `"<stance_name>": <value>` pair defines one of the possible "constructive truths" that the variable could hold. The `<stance_name>` **MUST** be a quoted string.
-   Each pair **MUST** be separated by a comma, just like a standard Python dictionary entry.

### 3.3. The `resolve` Statement

This is the operator that collapses a paraconsistent state into a classical one.

**Syntax:**
```plang
<resolved_variable> = resolve <paraconsistent_variable> with <stance_expression>
```

**Semantics:**
-   The `resolve` statement is an expression that evaluates to a single, classical value.
-   It takes a `<paraconsistent_variable>` (one that was defined in a `dialetheia` block).
-   The `<stance_expression>` must evaluate to a string that matches one of the `<stance_name>` keys within the `dialetheia` block.
-   The `resolve` expression returns the corresponding `<value>` for the chosen stance. After this statement, `<resolved_variable>` is a standard, classical variable.

## 4. Example

```plang
# 1. Define a paraconsistent variable 'db_config'
dialetheia db_config:
    Production: {
        "host": "prod.db.internal",
        "user": "prod_user",
        "timeout": 30
    }
    Development: {
        "host": "localhost",
        "user": "dev_user",
        "timeout": 5
    }

# 2. Define a stance for resolution
# In a real program, this might come from an environment variable or config file.
current_stance = "Production"

# 3. Resolve the contradiction based on the stance
# The 'active_config' variable will now hold a single, classical dictionary.
active_config = resolve db_config with current_stance

# 4. Use the resolved, classical variable
print(f"Connecting to database at: {active_config['host']}")
# Expected Output: "Connecting to database at: prod.db.internal"
```

## 5. Transpilation Strategy

P-Lang is not intended to be run by a native interpreter. It will be **transpiled** to standard Python. A transpiler (`plang_transpiler.py`) will perform the following transformations using an Abstract Syntax Tree (AST):

1.  A `dialetheia db_config:` block will be transformed into a standard Python dictionary:
    ```python
    db_config = {
        "Production": { ... },
        "Development": { ... }
    }
    ```
2.  A `resolve db_config with current_stance` statement will be transformed into a dictionary lookup:
    ```python
    active_config = db_config[current_stance]
    ```

This approach allows P-Lang to provide a clean, declarative syntax for handling contradictions while leveraging the full power and ecosystem of the underlying Python runtime.