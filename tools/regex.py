from typing import Any, Dict, FrozenSet, List, Set, Tuple
from functools import lru_cache
from tools.nfa import NFA

END = "$"
OPERATORS = {"|", ".", "*", "?"}


class Node():
    """ Node of the syntax tree generated by the RegExpParser class """

    def __init__(self, symbol: str, left, right, label) -> None:
        if symbol == '.' and left is None:
            self.symbol = right.symbol
            self.left = right.left
            self.right = right.right
        else:
            self.symbol = symbol
            self.left = left
            self.right = right
        self.label = label

    def __str__(self):
        return self.symbol + str(self.label)

    def __eq__(self, other):
        if other is None:
            return False
        return self.symbol == other.symbol and self.label == other.label

    def __hash__(self):
        return hash(self.label)

    @lru_cache(maxsize=128)
    def down(self, visited: FrozenSet[Any]=None) -> Set[Any]:
        """ Returns the set of reachable nodes by going down on this node """
        if visited is None:
            visited = frozenset()

        if self in visited:
            return {self} if self.symbol not in OPERATORS else set()

        visited |= {self}
        if self.symbol == "|":
            return self.left.down(visited) | self.right.down(visited)
        elif self.symbol == ".":
            return self.left.down(visited)
        elif self.symbol == "*" or self.symbol == "?":
            return self.left.down(visited) | self.right.up(visited)
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
        elif self.symbol == ".":
            return self.right.down(visited)
        elif self.symbol == "*":
            return self.left.down(visited) | self.right.up(visited)
        elif self.symbol == "?":
            return self.right.up(visited)
        elif self.symbol == END:
            return {self}
        else:
            raise RuntimeError(
                "Going up on invalid Node {}".format(self.symbol))


END_NODE = Node(END, None, None, 0)


class RegExpParser():
    """ Recursive descent regex parser """

    def __init__(self, regex: str) -> None:
        self._input_regex = regex.replace(".", "")
        self._pos = 0  # position of the next symbol
        self._nodes = 0  # number nodes created, used to label them

    def parse(self) -> Node:
        """ Returns the root node of the regex syntax tree """
        try:
            root = self._regex()
        except IndexError:
            raise RuntimeError("Invalid regex")

        if self._pos != len(self._input_regex):
            raise RuntimeError("Invalid regex")

        return root

    def _peek(self) -> str:
        return self._input_regex[self._pos]

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
        if self._more() and self._peek() == '|':
            self._eat('|')
            regex = self._regex()
            self._nodes += 1
            return Node('|', term, regex, self._nodes)
        return term

    def _term(self) -> Node:
        # <term> ::= { <factor> }
        factor = None
        while self._more() and self._peek() != ')' and self._peek() != '|':
            next_factor = self._factor()
            self._nodes += 1
            factor = Node('.', factor, next_factor, self._nodes)
        return factor

    def _factor(self) -> Node:
        # <factor> ::= <base> { '*' } | <base> { '?' }
        base = self._base()
        while self._more() and (self._peek() == '*' or self._peek() == '?'):
            peek = self._peek()
            self._eat(peek)
            self._nodes += 1
            base = Node(peek, base, None, self._nodes)
        return base

    def _base(self) -> Node:
        # <base> ::= <char> | '(' <regex> ')'
        if self._peek() == '(':
            self._eat('(')
            regex = self._regex()
            self._eat(')')
            return regex
        self._nodes += 1
        return Node(self._follow(), None, None, self._nodes)


def thread_tree(root: Node) -> None:
    """ Threads the tree, making it easy to follow in order from any node """
    stack = []  # type: List[Node]
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
    """
        Transforms a regular expression into a DFA using the De Simone/Aho
        method.
    """
    root = RegExpParser(regex).parse()
    thread_tree(root)

    if root is None:
        return NFA({"q0"}, set(), {}, "q0", {"q0"})

    alphabet = set()  # type: Set[str]
    transitions = {}  # type: Dict[Tuple[str, str], Set[str]]
    initial_state = "q0"
    final_states = set()  # type: Set[str]
    states = {initial_state}

    initial_nodes = root.down()
    compositions = {initial_state: initial_nodes}
    if END_NODE in compositions[initial_state]:
        final_states.add(initial_state)

    new_states = {initial_state}
    while new_states:
        symbols = {}  # type: Dict[str, Set[Node]]
        state = new_states.pop()

        # separate nodes of the same symbol
        for node in compositions[state]:
            if node.symbol != END:
                symbols.setdefault(node.symbol, set()).add(node)

        for symbol, nodes in symbols.items():
            alphabet.add(symbol)
            new_state = "q" + str(len(states))
            new_state_composition = set()  # type: Set[Node]

            # create composition of the new state, that is, the nodes of the
            # tree you're in, when you're in that state
            for node in nodes:
                new_state_composition.update(node.right.up())

            # if there's a state with the same composition, they're equivalent
            for existing_state, comp in compositions.items():
                if new_state_composition == comp:
                    new_state = existing_state

            # the new state is actually a new state
            if new_state not in states:
                states.add(new_state)
                new_states.add(new_state)
                compositions[new_state] = new_state_composition
                if END_NODE in new_state_composition:
                    final_states.add(new_state)

            transitions[state, symbol] = {new_state}

    Node.up.cache_clear()
    Node.down.cache_clear()
    return NFA(states, alphabet, transitions, initial_state, final_states)
