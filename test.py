import unittest
from typing import Set
from tools.nfa import NFA
from tools.grammar import RegularGrammar


class TestNFA(unittest.TestCase):

    def test_accept(self):
        def test(nfa: NFA, true_cases: Set[str], false_cases: Set[str]):
            self.assertTrue(all(nfa.accept(s) for s in true_cases))
            self.assertFalse(any(nfa.accept(s) for s in false_cases))

        nfa = NFA.load("examples/div3.json")
        true_cases = {"110100111", "111111000", "1110000001"}
        false_cases = {"1000000110", "110001", "1010001010"}
        test(nfa, true_cases, false_cases)

        nfa = NFA.load("examples/aaORbb.json")
        true_cases = {"baabaabab", "bbababbbab", "babaaaaba"}
        false_cases = {"", "aabb", "bbaa", "ababababaababababb"}
        test(nfa, true_cases, false_cases)

        nfa = NFA.load("examples/endsWbb.json")
        with self.assertRaises(RuntimeError):
            nfa.accept("aaaabb")


class testRG(unittest.TestCase):

    def test_nfa_to_rg_conversion(self):
        grammar = RegularGrammar.fromNFA(NFA.load("examples/div3.json"))
        self.assertTrue(grammar.initial_symbol() == "S'")
        self.assertTrue(
            grammar.productions() ==
            {
                "S'": {"0S", "1A", "0", "&"},
                "S":  {"0S", "1A", "0"},
                "A":  {"0B", "1S", "1"},
                "B":  {"0A", "1B"}
            })

        grammar = RegularGrammar.fromNFA(NFA.load("examples/endsWbb.json"))
        self.assertTrue(grammar.initial_symbol() == "S")
        self.assertTrue(
            grammar.productions() ==
            {
                "S": {"aS", "bS", "bA"},
                "A": {"b", "bB"}
            })

if __name__ == "__main__":
    unittest.main()
