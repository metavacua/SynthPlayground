# protocols/chc/protocol.py
from abc import ABC, abstractmethod

class CHCProtocol(ABC):
    """
    A base class for defining Curry-Howard Correspondence protocols.
    """

    @abstractmethod
    def get_proposition(self) -> str:
        """
        Returns a string representation of the protocol's proposition.
        """

    @abstractmethod
    def check_preconditions(self, state):
        """
        Checks if the preconditions for the protocol are met.
        """

    @abstractmethod
    def check_postconditions(self, initial_state, final_state):
        """
        Checks if the postconditions for the protocol are met.
        """

    @abstractmethod
    def check_invariants(self, initial_state, final_state):
        """
        Checks if the invariants of the protocol are maintained.
        """

    @abstractmethod
    def get_proof(self):
        """
        Returns the proof of the protocol.
        """

    @abstractmethod
    def get_initial_state(self):
        """
        Returns an initial state for the protocol.
        """
