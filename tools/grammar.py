from typing import Dict, List, Set
from tools.nfa import NFA


class RegularGrammar():

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
    def fromNFA(nfa: NFA):
        grammar = RegularGrammar()
        grammar._initial_symbol = nfa.initial_state()
        for k, v in nfa.transition_table().items():
            for state in v:
                if k[0] not in grammar._productions:
                    grammar._productions[k[0]] = set()
                grammar._productions[k[0]].add(k[1] + state)
                if state in nfa.final_states():
                    grammar._productions[k[0]].add(k[1])
        if nfa.initial_state() in nfa.final_states():
            grammar._productions[grammar._initial_symbol + "'"] = \
                grammar._productions.get(grammar._initial_symbol, set()) | \
                {"&"}
            grammar._initial_symbol = grammar._initial_symbol + "'"
        return grammar
