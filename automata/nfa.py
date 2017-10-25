from typing import Dict, List, Tuple, Set
import json

EPSILON = "&"


class NFA():

    def __init__(
            self,
            states: Set[str]=None,
            alphabet: Set[str]=None,
            transitions: Dict[Tuple[str, str], Set[str]]=None,
            initial_state: str="",
            final_states: Set[str]=None) -> None:
        self._states = states if states else set()
        self._alphabet = alphabet if alphabet else set()  # | set(EPSILON)
        self._transitions = transitions if transitions else {}
        self._initial_state = initial_state
        self._final_states = final_states if final_states else set()

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

    def accept(self, string: str) -> bool:
        """
            Checks if a given string is member of the language recognized by
            the NFA. Using non-deterministic transitions.
        """
        current_state = set([self._initial_state])

        for symbol in string:
            next_state = set()
            for state in current_state:
                next_state.update(self._transitions.setdefault((state, symbol),
                                                                set())
                                 )
            current_state = next_state

        return bool(current_state.intersection(self._final_states))

    def find_reachable(self, states: Set[str], symbol: str) -> Set[str]:
        """
            Given a set of states, applies a depth search algorithm
            to find the reachable states of them through transitions of the
            given symbol
        """
        found = set()
        for state in states:
            if (state, symbol) in self._transitions:
                found.update(self._transitions[(state, symbol)])
        return found

    def insert_deterministic_state(self, actual: Tuple[str, str], 
                                   states_set: Set[str]) -> None:
        """
            For a given set of states, verify whether they pertains to the 
            actual states of the FA. In negative case, add it and insert
            the transitions properly
        """
        name = ", ".join(str(s) for s in sorted(states_set))
        if (name not in self._states):
            self.add_state(name)
            for symbol in self._alphabet:
                reachable = self.find_reachable(states_set, symbol)
                self.insert_deterministic_state((name, symbol), reachable)

        self.set_transition(actual[0], actual[1], set([name]))

    def determinize(self) -> None:
        """
            Given the actual NFA, determinizes it, appending the new
            transitions and states to the actual ones of the NFA.
        """
        original_transitions = self._transitions.copy()

        for actual, next_state in original_transitions.items():
            self.insert_deterministic_state(actual, next_state)

    def save(self, path: str):
        data = {}
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
