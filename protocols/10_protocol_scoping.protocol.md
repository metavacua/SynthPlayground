# Protocol: Hierarchical Protocol Scoping

This protocol defines the agent's behavior regarding the loading and enforcement of `AGENTS.md` files in a hierarchical file structure. It is a fundamental principle of the agent's operation.

## The Principle of Proximity

The agent's governing protocols are determined by the `AGENTS.md` file that is "closest" to its current operational scope. When the agent performs an action on a file or directory, it adheres to the rules defined in the `AGENTS.md` file located in the deepest common parent directory.

- **Example:** If the agent is instructed to write to `/a/b/c.txt`, it will first look for an `AGENTS.md` in `/a/b/`. If not found, it will look in `/a/`, and finally in the root directory `/`.

This mechanism allows for both global, repository-wide protocols and fine-grained, module-specific overrides.

## Experimental Verification

This principle was empirically verified through an experiment (see `experiments/hierarchical_test` during development). An `AGENTS.md` file was placed in a subdirectory with a unique, observable rule. When the agent was tasked with an operation within that subdirectory, it correctly followed the local rule, demonstrating that the local `AGENTS.md` took precedence over the root `AGENTS.md`. This confirms that protocol loading is dynamically scoped to the file system hierarchy.