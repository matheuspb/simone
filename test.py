import unittest
from typing import Set
from tools.nfa import NFA
from tools.grammar import RegularGrammar
from tools.regex import regex_to_dfa


class TestNFA(unittest.TestCase):
    """ Tests NFA transformations """

    def nfa_test(self, nfa: NFA, true_cases: Set[str], false_cases: Set[str]) \
            -> None:
        self.assertTrue(all(nfa.accept(s) for s in true_cases))
        self.assertFalse(any(nfa.accept(s) for s in false_cases))

    def test_accept(self) -> None:
        nfa = NFA.load("examples/div3.json")
        true_cases = {"110100111", "111111000", "1110000001"}
        false_cases = {"1000000110", "110001", "1010001010", "211"}
        self.nfa_test(nfa, true_cases, false_cases)

        nfa = NFA.load("examples/aaORbb.json")
        true_cases = {"baabaabab", "bbababbbab", "babaaaaba"}
        false_cases = {"", "aabb", "bbaa", "ababababaababababb"}
        self.nfa_test(nfa, true_cases, false_cases)

    def test_minimization(self) -> None:
        nfa = NFA.load("examples/bdiv3.json")
        nfa.minimize()
        self.assertEqual(len(nfa.states), 3)
        true_cases = {"", "aa", "bbb", "abababa", "aaaaabbaababaaabb"}
        false_cases = {"ba", "bbaaa", "ababababa", "bbaaabb", "babbaaabba"}
        self.nfa_test(nfa, true_cases, false_cases)

        nfa = NFA.load("examples/one1.json")
        nfa.minimize()
        self.assertEqual(len(nfa.states), 2)
        true_cases = {"1", "01", "10", "000000000100000"}
        false_cases = {"", "0", "00", "11", "111", "0100001", "1000001"}
        self.nfa_test(nfa, true_cases, false_cases)

        nfa = NFA.load("examples/div5.json")
        nfa.determinize()
        nfa.minimize()
        self.assertEqual(len(nfa.states), 6)
        true_cases = {"0", "101", "1000101011"}
        false_cases = {"", "1", "101010111", "11101010"}
        self.nfa_test(nfa, true_cases, false_cases)

        with self.assertRaises(RuntimeError):
            nfa = NFA.load("examples/endsWbb.json")
            nfa.minimize()

    def test_emptiness(self) -> None:
        nfa = NFA.load("examples/one1.json")
        self.assertFalse(nfa.is_empty())
        self.assertFalse(nfa.is_finite())

        nfa = NFA.load("examples/bad_case.json")
        self.assertFalse(nfa.is_empty())
        self.assertFalse(nfa.is_finite())

        nfa = NFA.load("examples/aa.json")
        self.assertFalse(nfa.is_empty())
        self.assertTrue(nfa.is_finite())

        nfa = NFA.load("examples/empty.json")
        self.assertTrue(nfa.is_empty())

        nfa = NFA.load("examples/useless_loop.json")
        self.assertFalse(nfa.is_empty())
        self.assertTrue(nfa.is_finite())

        nfa = regex_to_dfa("aa|bbb|cccc")
        self.assertFalse(nfa.is_empty())
        self.assertTrue(nfa.is_finite())

    def test_determinization(self) -> None:
        nfa = NFA.load("examples/endsWbb.json")
        self.assertFalse(nfa.is_deterministic())
        true_cases = {"bb", "abaabbabaabb", "babb", "abbabbabb"}
        false_cases = {"", "abba", "bbbbbba", "bbbaaabba", "absbb"}
        self.nfa_test(nfa, true_cases, false_cases)
        nfa.determinize()
        self.assertTrue(nfa.is_deterministic())
        self.nfa_test(nfa, true_cases, false_cases)

        nfa = NFA.load("examples/bad_case.json")
        self.assertFalse(nfa.is_deterministic())
        true_cases = {"bb", "abaabbabaabb", "babb", "abbabbabb"}
        true_cases = {"baaa", "bbbb", "aababa", "bbbbbbbb"}
        false_cases = {"", "abbb", "aaaaaa"}
        self.nfa_test(nfa, true_cases, false_cases)
        nfa.determinize()
        self.assertTrue(nfa.is_deterministic())
        self.nfa_test(nfa, true_cases, false_cases)

    def test_dead_removal(self) -> None:
        nfa = NFA.load("examples/one1.json")
        self.assertTrue(nfa.states, set(['A', 'B', 'C', 'D', 'E', 'F']))
        nfa.remove_dead()
        self.assertTrue(nfa.states, set(['A', 'B', 'C', 'D', 'E']))

    def test_union(self) -> None:
        first_nfa = NFA.load("examples/aa.json")
        second_nfa = NFA.load("examples/endsWbb.json")

        first_nfa.union(second_nfa)
        self.assertTrue(first_nfa.accept("aa"))
        self.assertTrue(first_nfa.accept("abb"))
        self.assertTrue(first_nfa.accept("abbaabb"))
        self.assertFalse(first_nfa.accept("abbaab"))
        self.assertFalse(first_nfa.accept("ab"))
        self.assertFalse(first_nfa.accept("aaa"))

    def test_complement(self) -> None:
        nfa = NFA.load("examples/endsWbb.json")

        nfa.complement()
        self.assertTrue(nfa.accept("ab"))
        self.assertTrue(nfa.accept("babbaab"))
        self.assertFalse(nfa.accept("abb"))
        self.assertFalse(nfa.accept("aaabb"))

    def test_intersection(self) -> None:
        first_nfa = NFA.load("examples/aaORbb.json")
        second_nfa = NFA.load("examples/aa.json")

        first_nfa.intersection(second_nfa)
        self.assertTrue(first_nfa.accept("aa"))
        self.assertFalse(first_nfa.accept(""))
        self.assertFalse(first_nfa.accept("bb"))
        self.assertFalse(first_nfa.accept("bbaa"))

        first_nfa = NFA.load("examples/bb.json")
        second_nfa = NFA.load("examples/aa.json")

        first_nfa.intersection(second_nfa)
        self.assertTrue(first_nfa.is_empty())


class TestRG(unittest.TestCase):
    """ Tests NFA <-> regular grammar conversions """

    def test_nfa_to_rg_conversion(self) -> None:
        grammar = RegularGrammar.from_nfa(NFA.load("examples/div3.json"))
        self.assertTrue(grammar.initial_symbol() == "S'")
        self.assertTrue(
            grammar.productions() ==
            {
                "S'": {"0S", "1A", "0", "&"},
                "S":  {"0S", "1A", "0"},
                "A":  {"0B", "1S", "1"},
                "B":  {"0A", "1B"}
            })

        grammar = RegularGrammar.from_nfa(NFA.load("examples/endsWbb.json"))
        self.assertTrue(grammar.initial_symbol() == "S")
        self.assertTrue(
            grammar.productions() ==
            {
                "S": {"aS", "bS", "bA"},
                "A": {"b", "bB"}
            })

    def test_rg_to_nfa_conversion(self) -> None:
        grammar = RegularGrammar("S", {"S": {"&"}})
        nfa = NFA.from_regular_grammar(grammar)
        self.assertTrue(nfa.accept(""))

        test_nfa = TestNFA()

        grammar = RegularGrammar("S", {
            "S": {"0S", "1A", "0"},
            "A": {"0B", "1C"},
            "B": {"0D", "1S", "1"},
            "C": {"0A", "1B"},
            "D": {"0C", "1D"}
        })
        nfa = NFA.from_regular_grammar(grammar)
        true_cases = {"0", "101", "1000101011"}
        false_cases = {"", "1", "101010111", "11101010"}
        test_nfa.nfa_test(nfa, true_cases, false_cases)

        grammar = RegularGrammar("S'", {
            "S'": {"aA", "cC", "bA", "bC", "&"},
            "S": {"aA", "cC", "bA", "bC"},
            "A": {"bS", "cD", "b", "c"},
            "C": {"bS", "aE", "b", "a"},
            "D": {"aA", "bA", "bC"},
            "E": {"cC", "bC", "bA"},
        })
        nfa = NFA.from_regular_grammar(grammar)
        true_cases = {"", "abab", "caca", "abcabbbacb"}
        false_cases = {"aa", "cc", "bbb", "babcb"}
        test_nfa.nfa_test(nfa, true_cases, false_cases)


class TestRegex(unittest.TestCase):
    """ Tests the regular expression to DFA conversion """

    def test_regex_to_dfa(self) -> None:
        test_nfa = TestNFA()

        automata = regex_to_dfa("1?(01)*0?")
        self.assertTrue(automata.is_deterministic())
        test_nfa.nfa_test(
            automata,
            {"", "0", "1", "0101", "10101"},
            {"11", "00", "1010100", "010110101"})

        automata = regex_to_dfa("(a(ba)*a|ba)*(ab)*")
        self.assertTrue(automata.is_deterministic())
        test_nfa.nfa_test(
            automata,
            {"", "aa", "ab", "ba", "aaaa", "baaaab", "aabaababaaba"},
            {"a", "b", "bb", "aabbaa", "ababa", "baaab"})

        automata = regex_to_dfa("")
        self.assertTrue(automata.is_deterministic())
        test_nfa.nfa_test(automata, {""}, {"a", "ahgsdkjahsg"})

if __name__ == "__main__":
    unittest.main()
