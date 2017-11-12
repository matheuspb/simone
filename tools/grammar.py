from typing import Dict, Set


class RegularGrammar():
    """
        Regular grammar object, it is represented as a dictionary, for each non
        terminal symbol of the grammar, there is a dictionary entry with the
        corresponding strings that it can derive.

        For example, the grammar:
        S -> aA | bB | a | b
        A -> aA | a
        B -> bB | b

        is represented as:
        {
            "S": {"aA", "bB", "a", "b"},
            "A": {"aA", "a"},
            "B": {"bB", "b"}
        }
    """

    def __init__(
            self, initial_symbol: str="",
            productions: Dict[str, Set[str]]=None) -> None:
        self._initial_symbol = initial_symbol
        self._productions = productions if productions else {}

    def initial_symbol(self):
        return self._initial_symbol

    def productions(self):
        return self._productions

    @staticmethod
    def from_nfa(nfa) -> 'RegularGrammar':
        """
            Returns a regular grammar that generates the language of the given
            NFA
        """
        initial_symbol = nfa.initial_state
        productions = {}  # type: Dict[str, Set[str]]

        # if delta(A, a) = B, then add the production A -> aB to the grammar
        # if B is a final state of the NFA then also add A -> a
        for k, states in nfa.transition_table.items():
            for state in states:
                if k[0] not in productions:
                    productions[k[0]] = set()
                productions[k[0]].add(k[1] + state)
                if state in nfa.final_states:
                    productions[k[0]].add(k[1])

        # if the NFA accepts epsilon, add epsilon to the grammar
        if nfa.initial_state in nfa.final_states:
            new_initial_symbol = initial_symbol + "'"
            productions[new_initial_symbol] = \
                productions.get(initial_symbol, set()) | {"&"}
            initial_symbol = new_initial_symbol

        return RegularGrammar(initial_symbol, productions)
