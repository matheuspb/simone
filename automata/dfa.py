from itertools import product
from typing import Dict, List, Tuple, Set


class DFA():

    def __init__(
            self, states: Set[str], alphabet: Set[str], initial_state: str,
            accept_states: Set[str], transitions: Dict[Tuple[str, str], str])\
            -> None:
        self._states = states
        self._alphabet = alphabet
        self._transitions = transitions
        self._initial_state = initial_state
        self._accept_states = accept_states

    def transition_table(self) -> Dict[Tuple[str, str], str]:
        return self._transitions

    def states(self) -> List[str]:
        return sorted(self._states)

    def alphabet(self) -> List[str]:
        return sorted(self._alphabet)

    def add_symbol(self, symbol: str) -> None:
        self._alphabet.add(symbol)

    def add_state(self, state: str) -> None:
        self._states.add(state)
