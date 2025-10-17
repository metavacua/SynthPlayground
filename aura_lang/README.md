# Aura Programming Language

Aura is a small, dynamically-typed scripting language.

## Features

*   **Variables**: Declare variables with `let`.
*   **Data Types**: Integers, Booleans, Strings.
*   **Operators**: `+`, `-`, `*`, `/`, `<`, `>`.
*   **Control Flow**: `if`/`else` expressions.
*   **Functions**: Define named functions with the `func` keyword. First-class functions are not supported.
*   **Built-ins**: `len()` for strings.

## Syntax

### Variable Declaration
```aura
let x = 5;
let y = "hello";
```

### Function Definition
```aura
func add(a, b) {
  return a + b;
}

let result = add(2, 3);
```

### Conditional
```aura
if (x > y) {
  return x;
} else {
  return y;
}
```