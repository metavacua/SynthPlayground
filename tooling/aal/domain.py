# tooling/aal/domain.py

from dataclasses import dataclass
from typing import Set, FrozenSet


@dataclass(frozen=True)
class Fluent:
    """Represents a fluent (a proposition) in the domain."""

    name: str


@dataclass(frozen=True)
class Action:
    """Represents an action that can be performed by an agent."""

    name: str


@dataclass(frozen=True)
class CausalLaw:
    """Represents a causal law of the form 'a causes f if p1, ..., pn'."""

    action: Action
    effect: Fluent
    conditions: FrozenSet[Fluent]


@dataclass
class Domain:
    """Represents a complete AAL domain description."""

    fluents: Set[Fluent]
    actions: Set[Action]
    causal_laws: Set[CausalLaw]

    def __init__(self):
        self.fluents = set()
        self.actions = set()
        self.causal_laws = set()
