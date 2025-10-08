class ParaconsistentVariable:
    """
    A class to represent a variable in a paraconsistent state, holding
    multiple, mutually exclusive potential values.
    """

    def __init__(self, states: dict):
        """
        Initializes the variable with a dictionary of possible states.

        Args:
            states (dict): A dictionary where keys are stance names (e.g., "Safety")
                           and values are the corresponding potential values.
        """
        if not isinstance(states, dict) or not states:
            raise ValueError(
                "ParaconsistentVariable must be initialized with a non-empty dictionary of states."
            )
        self._states = states

    def resolve(self, stance: str):
        """
        Resolves the contradiction by selecting a value based on the given stance.

        Args:
            stance (str): The name of the stance to resolve with.

        Returns:
            The value corresponding to the chosen stance.

        Raises:
            KeyError: If the provided stance does not exist in the variable's states.
        """
        if stance not in self._states:
            raise KeyError(
                f"Stance '{stance}' not found. Available stances are: {list(self._states.keys())}"
            )
        return self._states[stance]

    def __repr__(self):
        return f"ParaconsistentVariable(stances={list(self._states.keys())})"
