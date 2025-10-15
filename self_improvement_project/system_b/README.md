# System B: The Curator Who Cannot Create

## Principle

This system demonstrates the other side of the Tarski-inspired dichotomy:
*   **Definable Set of Names:** The system can read and write to its `state.json` file. It has a perfect, complete, and definable understanding of its own state.
*   **Undefinable Diagonalization Function:** The `run.py` script has **no internal function for creating new elements**. The act of creation must come from outside the system.

## How to Run

To run the curation process, you must provide a new element from an external source as a command-line argument:

```bash
# This will succeed
python3 self_improvement_project/system_b/run.py "a_brand_new_idea"

# This will be rejected as a duplicate
python3 self_improvement_project/system_b/run.py "initial_element"

# This will fail, as the system cannot create on its own
python3 self_improvement_project/system_b/run.py
```
The system will check if the provided element is truly new and, if so, add it to its `state.json` file.