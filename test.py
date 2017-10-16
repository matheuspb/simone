import unittest
from typing import Set
from automata.nfa import NFA


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

if __name__ == "__main__":
    unittest.main()
