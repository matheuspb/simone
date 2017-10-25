from typing import Dict, List, Tuple, Set, Any
import json


class NFA():

    def __init__(
            self,
            states: Set[str]=None,
            alphabet: Set[str]=None,
            transitions: Dict[Tuple[str, str], Set[str]]=None,
            initial_state: str="",
            final_states: Set[str]=None) -> None:
        self._states = states if states else set()
        self._alphabet = alphabet if alphabet else set()
        self._transitions = transitions if transitions else {}
        self._initial_state = initial_state
        self._final_states = final_states if final_states else set()

    def transition_table(self) -> Dict[Tuple[str, str], Set[str]]:
        return self._transitions

    def states(self) -> List[str]:
        return [self._initial_state] + \
            sorted(self._states - {self._initial_state})

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
        for state in self._states:
            # remove transitions by the removed symbol
            if (state, symbol) in self._transitions:
                del self._transitions[state, symbol]

    def add_state(self, state: str) -> None:
        if not self._initial_state:
            self._initial_state = state
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
        if not next_states:
            # assert transition won't exist
            self._transitions.pop((state, symbol), set())
        elif next_states <= self._states:
            self._transitions[state, symbol] = next_states
        else:
            states = ", ".join(next_states - self._states)
            raise KeyError("State(s) {} do not exist".format(states))

    """ Removes the states that the automaton will never be in """
    def remove_unreachable(self) -> None:
        reachable = set()  # type: Set[str]
        new_reachable = {self._initial_state}
        while not new_reachable <= reachable:
            reachable |= new_reachable
            n = new_reachable.copy()
            new_reachable = set()
            for state in n:
                for symbol in self._alphabet:
                    new_reachable.update(
                        self._transitions.get((state, symbol), set()))

        unreachable_states = self._states - reachable
        for unreachable_state in unreachable_states:
            self.remove_state(unreachable_state)

    """ Removes states that never reach a final state """
    def remove_dead(self) -> None:
        # assumes all unreachable states were removed
        alive_states = self._final_states.copy()
        self._is_alive(self._initial_state, alive_states, set())
        for dead_state in self._states - alive_states:
            self.remove_state(dead_state)

    """
        Uses the recursive definition of alive state, that is, if you can reach
        an alive state from the state, it is alive. The initial set of alive
        states are the final states.

        The visited set is used just to avoid an infinite recursion.
    """
    def _is_alive(self, state: str, alive: Set[str], visited: Set[str]):
        if state not in visited:
            visited.add(state)
            reachable_states = set()  # type: Set[str]
            for symbol in self._alphabet:
                reachable_states.update(
                    self._transitions.get((state, symbol), set()))
            for reachable_state in reachable_states:
                if self._is_alive(reachable_state, alive, visited):
                    alive.add(state)
        return state in alive

    def accept(self, string: str) -> bool:
        current_state = self._initial_state
        try:
            for symbol in string:
                next_state = self._transitions[current_state, symbol]
                if len(next_state) == 1:
                    current_state = next(iter(next_state))
                else:
                    raise RuntimeError(
                        "Reached a non-deterministic transition")
        except KeyError:
            # undefined transition
            return False
        return current_state in self._final_states

    # TODO unit tests
    @staticmethod
    def from_regular_grammar(grammar):
        initial_symbol = grammar.initial_symbol()
        productions = grammar.productions()

        states = set(productions.keys()) | {"X"}
        alphabet = set()
        transitions = {}
        initial_state = initial_symbol
        final_states = set("X") | \
            ({initial_symbol} if "&" in productions[initial_symbol] else set())

        for non_terminal, prods in productions.items():
            for production in prods:
                if production == "&":
                    continue

                new_transition = "X" if len(production) == 1 else production[1]
                transitions.setdefault(
                    (non_terminal, production[0]), set()).add(new_transition)

                alphabet.add(production[0])

        return NFA(states, alphabet, transitions, initial_state, final_states)

    def save(self, path: str):
        data = {}  # type: Dict[str, Any]
        data["states"] = sorted(self._states)
        data["alphabet"] = sorted(self._alphabet)
        data["transitions"] = \
            [(k[0], k[1], sorted(v)) for k, v in self._transitions.items()]
        data["initial_state"] = self._initial_state
        data["final_states"] = sorted(self._final_states)
        with open(path, 'w') as automata_file:
            json.dump(data, automata_file, indent=4)

    @staticmethod
    def load(path: str):
        with open(path, 'r') as automata_file:
            data = json.load(automata_file)
        states = set(data["states"])
        alphabet = set(data["alphabet"])
        transitions = {(v[0], v[1]): set(v[2]) for v in data["transitions"]}
        initial_state = data["initial_state"]
        final_states = set(data["final_states"])
        return NFA(
            states, alphabet, transitions, initial_state, final_states)
