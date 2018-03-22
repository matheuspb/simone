from typing import Any, Dict, FrozenSet, List, Set, Tuple
from functools import lru_cache
from collections import defaultdict
import re
from tools.nfa import NFA

END = "$"
EPSILON = "&"
OPERATORS = {"|", ".", "*", "?"}
TERMINALS_PATTERN = re.compile(r"[A-z0-9&]")


class Node():
    """ Node of the syntax tree generated by the RegExpParser class """

    _n_nodes = 0  # number of nodes built

    def __init__(self, symbol: str, left, right) -> None:
        self.symbol = symbol
        self.left = left
        self.right = right
        self._label = Node._n_nodes
        Node._n_nodes += 1

    def __hash__(self):
        return self._label

    @lru_cache(maxsize=128)
    def down(self, visited: FrozenSet[Any]=None) -> Set[Any]:
        """ Returns the set of reachable nodes by going down on this node """
        if visited is None:
            visited = frozenset()

        if self in visited:
            return {self} if self.symbol not in OPERATORS else set()

        visited |= {self}
        if self.symbol == '|':
            return self.left.down(visited) | self.right.down(visited)
        elif self.symbol == '.':
            return self.left.down(visited)
        elif self.symbol == '*' or self.symbol == '?':
            return self.left.down(visited) | self.right.up(visited)
        elif self.symbol == EPSILON:
            return self.right.up(visited)
        return {self}

    @lru_cache(maxsize=128)
    def up(self, visited: FrozenSet[Any]=None) -> Set[Any]:
        """ Returns the set of reachable nodes by going up on this node """
        if visited is None:
            visited = frozenset()

        if self.symbol == '|':
            # skip the whole right sub tree
            node = self.right
            while node.symbol == '.' or node.symbol == '|':
                node = node.right
            return node.right.up(visited)
        elif self.symbol == '.':
            return self.right.down(visited)
        elif self.symbol == '*':
            return self.left.down(visited) | self.right.up(visited)
        elif self.symbol == '?':
            return self.right.up(visited)
        # if self.symbol == END:
        return {self}


END_NODE = Node(END, None, None)


class RegExpParser():
    """ Recursive descent regex parser """

    def __init__(self, regex: str) -> None:
        self._input_regex = regex.replace(".", "")
        self._pos = 0  # position of the next symbol

    def parse(self) -> Node:
        """ Returns the root node of the regex syntax tree """
        root = self._regex()

        if self._pos != len(self._input_regex):
            raise RuntimeError("Invalid regex")

        return root

    def _peek(self) -> str:
        return self._input_regex[self._pos] \
            if self._pos < len(self._input_regex) \
            else ''

    def _eat(self, char: str) -> None:
        if self._peek() == char:
            self._pos += 1
        else:
            raise RuntimeError("Invalid regex")

    def _follow(self) -> str:
        char = self._peek()
        self._eat(char)
        return char

    def _more(self) -> bool:
        return self._pos < len(self._input_regex)

    def _regex(self) -> Node:
        # <regex> ::= <term> '|' <regex> | <term>
        term = self._term()
        if self._peek() == '|':
            self._follow()
            regex = self._regex()
            return Node('|', term, regex)
        return term

    def _term(self) -> Node:
        # <term> ::= <factor> <term> | <factor>
        factor = self._factor()
        if self._more() and self._peek() != ')' and self._peek() != '|':
            term = self._term()
            factor = Node('.', factor, term)
        return factor

    def _factor(self) -> Node:
        # <factor> ::= <base> { '*' } | <base> { '?' }
        base = self._base()
        while self._more() and (self._peek() == '*' or self._peek() == '?'):
            base = Node(self._follow(), base, None)
        return base

    def _base(self) -> Node:
        # <base> ::= <char> | '(' <regex> ')'
        if TERMINALS_PATTERN.match(self._peek()):
            return Node(self._follow(), None, None)
        elif self._peek() == '(':
            self._eat('(')
            regex = self._regex()
            self._eat(')')
            return regex
        else:
            raise RuntimeError("Invalid regex")


def thread_tree(root: Node) -> None:
    """ Threads the tree, making it easy to follow in order from any node """
    stack: List[Node] = []
    node = root
    # traverse the tree in order
    while stack or node:
        if node:
            stack.append(node)
            node = node.left
        else:
            node = stack.pop()
            if node.right is None:
                node.right = stack[-1] if stack else END_NODE
                node = None
            else:
                node = node.right


def regex_to_dfa(regex: str) -> NFA:
    """ Transforms a RegExp into a DFA using the De Simone/Aho method. """
    root = RegExpParser(regex).parse()
    thread_tree(root)

    alphabet: Set[str] = set()
    transitions: Dict[Tuple[str, str], Set[str]] = {}
    initial_state = "q0"
    final_states: Set[str] = set()
    states = {initial_state}

    initial_nodes = frozenset(root.down())
    compositions = {initial_nodes: initial_state}
    if END_NODE in initial_nodes:
        final_states.add(initial_state)

    new_compositions = {initial_nodes}
    while new_compositions:
        symbols: Dict[str, Set[Node]] = defaultdict(set)
        composition = new_compositions.pop()  # composition of the new state

        # separate nodes of the same symbol
        for node in composition:
            if node.symbol != END:
                symbols[node.symbol].add(node)

        # build the new state transitions
        for symbol, nodes in symbols.items():
            # create composition of the new state, that is, the nodes of the
            # tree you're in, when you're in that state
            new_state_composition: Set[Node] = set()
            for node in nodes:
                new_state_composition.update(node.right.up())
            frozen_new_composition = frozenset(new_state_composition)

            # if there's a state with the same composition, they're equivalent,
            # no need to create another one
            if frozen_new_composition in compositions:
                new_state = compositions[frozen_new_composition]
            else:  # else, create the new state
                new_state = "q" + str(len(compositions))
                compositions[frozen_new_composition] = new_state
                new_compositions.add(frozen_new_composition)
                if END_NODE in frozen_new_composition:
                    final_states.add(new_state)

            transitions[compositions[composition], symbol] = {new_state}

    for (state, symbol), next_state in transitions.items():
        states.update({state} | next_state)
        alphabet.add(symbol)

    Node.up.cache_clear()
    Node.down.cache_clear()
    return NFA(states, alphabet, transitions, initial_state, final_states)
