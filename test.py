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

        nfa = regex_to_dfa("aaa*|a*")
        nfa.minimize()
        self.assertEqual(len(nfa.states), 1)

        nfa = NFA.load("examples/endsWbb.json")
        with self.assertRaises(RuntimeError):
            nfa.minimize()
        with self.assertRaises(RuntimeError):
            nfa.merge_equivalent()

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
        true_cases = {
            "babb", "abbabbabb", "baaa", "bbbb", "aababa", "bbbbbbbb"}
        false_cases = {"", "abbb", "aaaaaa"}
        self.nfa_test(nfa, true_cases, false_cases)
        nfa.determinize()
        self.assertTrue(nfa.is_deterministic())
        self.nfa_test(nfa, true_cases, false_cases)

    def test_dead_removal(self) -> None:
        nfa = NFA.load("examples/one1.json")
        self.assertEqual(nfa.states, ['A', 'B', 'C', 'D', 'E', 'F'])
        nfa.remove_dead()
        self.assertEqual(nfa.states, ['A', 'B', 'C', 'D', 'E'])

    def test_union(self) -> None:
        first_nfa = NFA.load("examples/aa.json")
        second_nfa = NFA.load("examples/endsWbb.json")

        first_nfa.union(second_nfa)
        self.nfa_test(
            first_nfa, {"aa", "abb", "abbaabb"}, {"abbaab", "ab", "aaa"})

    def test_complement(self) -> None:
        nfa = NFA.load("examples/endsWbb.json")

        nfa.complement()
        self.nfa_test(
            nfa, {"ab", "babbaab"}, {"abb", "aaabb"})

    def test_intersection(self) -> None:
        first_nfa = NFA.load("examples/aaORbb.json")
        second_nfa = NFA.load("examples/aa.json")

        first_nfa.intersection(second_nfa)
        self.nfa_test(first_nfa, {"aa"}, {"", "bb", "bbaa"})

        first_nfa = NFA.load("examples/bb.json")
        second_nfa = NFA.load("examples/aa.json")

        first_nfa.intersection(second_nfa)
        self.assertTrue(first_nfa.is_empty())

        first_nfa = regex_to_dfa("a")
        second_nfa = regex_to_dfa("b")
        first_nfa.intersection(second_nfa)
        self.assertTrue(first_nfa.is_empty())

    def test_containment(self) -> None:
        first_nfa = NFA.load("examples/aaORbb.json")
        second_nfa = NFA.load("examples/aa.json")

        self.assertTrue(first_nfa.contains(second_nfa))
        self.assertFalse(second_nfa.contains(first_nfa))

    def test_equivalence(self) -> None:
        first_nfa = NFA.load("examples/aaORbb.json")
        second_nfa = NFA.load("examples/one1.json")

        self.assertFalse(first_nfa.is_equal(second_nfa))
        self.assertFalse(second_nfa.is_equal(first_nfa))
        self.assertTrue(first_nfa.is_equal(first_nfa))
        self.assertTrue(second_nfa.is_equal(second_nfa))


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

        def test_regex(
                regex: str, true_cases: Set[str], false_cases: Set[str]) \
                -> None:
            automata = regex_to_dfa(regex)
            self.assertTrue(automata.is_deterministic())
            test_nfa.nfa_test(automata, true_cases, false_cases)

        def test_bad_regex(regex: str) -> None:
            with self.assertRaises(RuntimeError):
                regex_to_dfa(regex)

        test_nfa = TestNFA()

        test_regex(
            "1?(01)*0?",
            {"", "0", "1", "0101", "10101"},
            {"11", "00", "1010100", "010110101"})
        test_regex(
            "(a(ba)*a|ba)*(ab)*",
            {"", "aa", "ab", "ba", "aaaa", "baaaab", "aabaababaaba"},
            {"a", "b", "bb", "aabbaa", "ababa", "baaab"})
        test_regex("&", {""}, {"a", "ahgsdkjahsg"})
        test_regex("a|&", {"", "a"}, {"aa", "ab"})
        test_regex("a|b|&", {"a", "b"}, {"ba", "bb"})
        test_regex("a**", {"", "a", "aaaa"}, {"b", "bbc"})
        test_regex("(a|b)*b", {"b", "aaab", "bbb"}, {"", "a", "aaa", "bba"})

        test_bad_regex("*")
        test_bad_regex("?")
        test_bad_regex("(a(a|b)*")
        test_bad_regex("a(a))*")
        test_bad_regex("((((a|&")
        test_bad_regex("(a)))")

if __name__ == "__main__":
    unittest.main()
