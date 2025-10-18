# Agent Action Language (AAL) Specification

## Syntax

An AAL domain description is a text file consisting of three types of declarations:

### 1. Fluent Declarations
A fluent is a proposition about the world that can be true or false.
```
fluent <fluent_name>
```

### 2. Action Declarations
An action is something an agent can perform.
```
action <action_name>
```

### 3. Causal Law Declarations
A causal law specifies the effects of an action.
```
<action_name> causes <fluent_name> if <fluent_1>, <fluent_2>, ..., <fluent_n>
```
If an action has no preconditions, the `if` part is omitted.

## Semantics

The state of the world is represented by a set of fluents. The AAL interpreter calculates the next state based on the current state and a given action by applying the causal laws. A fluent holds in the next state if and only if a causal law exists for the performed action whose conditions are met by the current state.
