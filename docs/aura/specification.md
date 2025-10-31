# Aura Language Specification

## 1. Introduction

Aura is a scripting language designed for orchestrating agentic workflows. It provides a simple, expressive syntax for defining complex behaviors, and a powerful, secure mechanism for interacting with the agent's core tools.

## 2. Syntax

Aura uses a C-style syntax. Statements are terminated with semicolons, and code blocks are enclosed in curly braces.

### 2.1. Comments

Single-line comments start with `//`.

```aura
// This is a comment
```

### 2.2. Variables

Variables are declared with the `let` keyword.

```aura
let x = 5;
let y = "hello";
```

## 3. Data Types

Aura supports the following data types:

- **Integer:** `10`, `-5`
- **String:** `"hello"`, `'world'`
- **Boolean:** `true`, `false`
- **Null:** `null`
- **Array:** `[1, 2, 3]`
- **Hash:** `{"a": 1, "b": 2}`

## 4. Control Flow

### 4.1. If-Else

```aura
if (x > 5) {
  print("x is greater than 5");
} else {
  print("x is not greater than 5");
};
```

### 4.2. Functions

Functions are defined with the `func` keyword.

```aura
func my_func(a, b) {
  return a + b;
};

let result = my_func(1, 2);
```

### 4.3. Typed Parameters and Return Types

Functions can also have typed parameters and return types.

```aura
func my_func(a: int, b: str) -> bool {
  return true;
};
```

## 5. Standard Library

Aura provides a small standard library of built-in functions.

- `print(...)`: Prints its arguments to the console.
- `len(obj)`: Returns the length of a string or array.

## 6. Agent Tool API

Aura scripts can call the agent's tools using the `agent_call_tool` function.

```aura
let result = agent_call_tool("my_tool", "arg1", "arg2");
```
