from typing import Dict, List, Tuple, Set

EPSILON = "ε"


class NFA():

    def __init__(
            self,
            states: Set[str],
            alphabet: Set[str],
            transitions: Dict[Tuple[str, str], Set[str]],
            initial_state: str,
            final_states: Set[str]) -> None:
        self._states = states
        self._alphabet = alphabet  # | set(EPSILON)
        self._transitions = transitions
        self._initial_state = initial_state
        self._final_states = final_states

    def transition_table(self) -> Dict[Tuple[str, str], Set[str]]:
        return self._transitions

    def states(self) -> List[str]:
        return sorted(self._states)

    def initial_state(self) -> str:
        return self._initial_state

    def final_states(self) -> Set[str]:
        return self._final_states

    def alphabet(self) -> List[str]:
        return sorted(self._alphabet)

    def add_symbol(self, symbol: str) -> None:
        self._alphabet.add(symbol)

    def remove_symbol(self, symbol: str) -> None:
        self._alphabet.discard(symbol)

    def add_state(self, state: str) -> None:
        self._states.add(state)

    def remove_state(self, state: str) -> None:
        # may not remove initial state
        if state != self._initial_state:
            self._states.discard(state)
            self._final_states.discard(state)
            for transition in self._transitions.values():
                # remove transitions that go to the removed state
                transition.discard(state)
            for symbol in self._alphabet:
                # remove useless transitions that come from the removed state
                if (state, symbol) in self._transitions:
                    del self._transitions[state, symbol]

    def toggle_final_state(self, state: str) -> None:
        if state in self._states:
            if state in self._final_states:
                self._final_states.remove(state)
            else:
                self._final_states.add(state)

    def set_transition(
            self, state: str, symbol: str, next_states: Set[str]) -> None:
        if next_states <= self._states:
            self._transitions[(state, symbol)] = next_states
        else:
            states = ", ".join(next_states - self._states)
            raise KeyError("State(s) {} do not exist".format(states))

    def accept(self, string: str) -> bool:
        current_state = self._initial_state
        try:
            for symbol in string:
                next_state = self._transitions[current_state, symbol]
                if len(next_state) == 1:
                    current_state = next(iter(next_state))
                else:
                    raise RuntimeError("Automata is non-deterministic")
        except KeyError:
            # undefined transition
            return False
        return current_state in self._final_states
