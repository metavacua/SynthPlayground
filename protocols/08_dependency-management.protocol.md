# Protocol: Initial Environment Setup

This protocol defines the mandatory first step for ensuring a consistent and correct development environment at the start of any task.

**Rule `dependency-install-mandate`**: Before any other action, if a `requirements.txt` file exists in the repository, you MUST run `pip install -r requirements.txt`. This action is critical to prevent `ModuleNotFoundError` errors during test execution or tool operation.

This proactive step ensures that all required dependencies are present, preventing a common class of failures and ensuring that subsequent steps operate on a known, stable baseline. It is a foundational element of a robust and reliable workflow.