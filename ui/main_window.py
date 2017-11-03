from typing import Set
import re
from ui.main_window_ui import Ui_MainWindow
from tools.nfa import NFA
from tools.grammar import RegularGrammar
from tools.regex import regex_to_dfa
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QInputDialog, QMessageBox, QFileDialog)

GRAMMAR_PATTERN = re.compile(r"^[A-Z]'?->[a-z0-9&][A-Z]?(\|[a-z0-9&][A-Z]?)*$")


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.resize(600, 400)

        self.regexToDFAButton.clicked.connect(self._regex_to_dfa)

        self.addSymbolButton.clicked.connect(self._add_symbols)
        self.addStateButton.clicked.connect(self._add_states)
        self.removeSymbolButton.clicked.connect(self._remove_symbol)
        self.removeStateButton.clicked.connect(self._remove_state)
        self.finalStateButton.clicked.connect(self._toggle_final_state)

        self.fromNFAbutton.clicked.connect(self._nfa_to_grammar)
        self.toNFAbutton.clicked.connect(self._grammar_to_nfa)

        self.testButton.clicked.connect(self._test_string)

        self.actionNew.triggered.connect(self._new)
        self.actionOpen.triggered.connect(self._open)
        self.actionSave.triggered.connect(self._save)

        self.actionDeterminize.triggered.connect(self._determinize)

        self.actionRemove_unreachable_states.triggered.connect(
            self._remove_unreachable)
        self.actionRemove_dead_states.triggered.connect(self._remove_dead)
        self.actionMerge_equivalent_states.triggered.connect(
            self._merge_equivalent)
        self.actionFull_minimization.triggered.connect(self._minimize)

        self.action_to_abc.triggered.connect(self._beautify_abc)
        self.action_to_qn.triggered.connect(self._beautify_qn)

        self.actionUnion.triggered.connect(self._union)
        self.actionComplement.triggered.connect(self._complement)
        self.actionIntersection.triggered.connect(self._intersection)

        self.transitionTable.cellChanged.connect(self._update_nfa)

        self._grammar = RegularGrammar()
        self._nfa = NFA()
        self._update_table()

    def _regex_to_dfa(self) -> None:
        try:
            self._nfa = regex_to_dfa(self.regexInput.text())
            self._update_table()
        except RuntimeError as error:
            QMessageBox.information(self, "Error", error.args[0])

    def _add_symbols(self) -> None:
        text, ok = QInputDialog.getText(
            self, "Add symbols", "Symbols (a,b,c,...):")
        if ok:
            for symbol in text.replace(" ", "").split(","):
                self._nfa.add_symbol(symbol)
            self._update_table()

    def _add_states(self) -> None:
        text, ok = QInputDialog.getText(
            self, "Add states", "States (q0,q1,...):")
        if ok:
            for state in text.replace(" ", "").split(","):
                self._nfa.add_state(state)
            self._update_table()

    def _remove_symbol(self) -> None:
        text, ok = QInputDialog.getText(self, "Remove symbol", "Symbol:")
        if ok:
            self._nfa.remove_symbol(text)
            self._update_table()

    def _remove_state(self) -> None:
        text, ok = QInputDialog.getText(self, "Remove state", "State:")
        if ok:
            self._nfa.remove_state(text)
            self._update_table()

    def _toggle_final_state(self) -> None:
        text, ok = QInputDialog.getText(self, "Final state", "State:")
        if ok:
            self._nfa.toggle_final_state(text)
            self._update_table()

    def _test_emptiness(self) -> None:
        if self._nfa.is_empty():
            self.languageLabel.setText("The language is empty.")
        elif self._nfa.is_finite():
            self.languageLabel.setText("The language is finite.")
        else:
            self.languageLabel.setText("The language is infinite.")

    def _remove_unreachable(self) -> None:
        self._nfa.remove_unreachable()
        self._update_table()

    def _remove_dead(self) -> None:
        self._nfa.remove_dead()
        self._update_table()

    def _merge_equivalent(self) -> None:
        try:
            self._nfa.merge_equivalent()
            self._update_table()
        except RuntimeError as error:
            QMessageBox.information(self, "Error", error.args[0])

    def _minimize(self) -> None:
        try:
            self._nfa.minimize()
            self._update_table()
        except RuntimeError as error:
            QMessageBox.information(self, "Error", error.args[0])

    def _test_string(self) -> None:
        try:
            self.statusbar.showMessage(
                "String accepted" if self._nfa.accept(self.inputString.text())
                else "String rejected")
        except RuntimeError as error:
            QMessageBox.information(self, "Error", error.args[0])

    def _determinize(self) -> None:
        self._nfa.determinize()
        self._update_table()

    def _beautify_qn(self) -> None:
        self._nfa.beautify_qn()
        self._update_table()

    def _beautify_abc(self) -> None:
        try:
            self._nfa.beautify_abc()
            self._update_table()
        except RuntimeError as error:
            QMessageBox.information(self, "Error", error.args[0])

    def _nfa_to_grammar(self) -> None:
        self._grammar = RegularGrammar.from_nfa(self._nfa)
        self._update_grammar_text()

    def _grammar_to_nfa(self) -> None:
        try:
            self._nfa = NFA.from_regular_grammar(
                parse_grammar_text(self.grammarText.toPlainText()))
            self._update_table()
        except RuntimeError as error:
            QMessageBox.information(self, "Error", error.args[0])

    def _union(self) -> None:
        pass

    def _complement(self) -> None:
        self._nfa.complement()
        self._update_table()

    def _intersection(self) -> None:
        pass

    def _update_nfa(self, row: int, col: int) -> None:
        states = self._nfa.states
        alphabet = self._nfa.alphabet
        next_states = \
            set(self.transitionTable.item(row, col).text().replace(
                " ", "").split(","))

        try:
            self._nfa.set_transition(
                states[row], alphabet[col],
                next_states if next_states != {""} else set())
        except KeyError as error:
            QMessageBox.information(self, "Error", error.args[0])
            self.transitionTable.item(row, col).setText("")

        self._test_emptiness()

    def _update_table(self) -> None:
        states = []
        for state in self._nfa.states:
            preffix = ""
            if state in self._nfa.final_states:
                preffix += "*"
            if state == self._nfa.initial_state:
                preffix += "->"
            states.append(preffix + state)

        alphabet = self._nfa.alphabet

        self.transitionTable.setRowCount(len(states))
        self.transitionTable.setVerticalHeaderLabels(states)

        self.transitionTable.setColumnCount(len(alphabet))
        self.transitionTable.setHorizontalHeaderLabels(alphabet)

        table = self._nfa.transition_table
        for i, state in enumerate(self._nfa.states):
            for j, symbol in enumerate(alphabet):
                transition = ",".join(sorted(table[state, symbol])) \
                    if (state, symbol) in table else ""
                self.transitionTable.setItem(
                    i, j, QTableWidgetItem(transition))

        self._test_emptiness()

    def _update_grammar_text(self) -> None:
        """
            "B", {"aB", "bC", "a"} turns into
            "B -> aB | bC | a"
        """
        def transform_production(non_terminal: str, productions: Set[str]):
            return "{} -> {}".format(
                non_terminal, " | ".join(sorted(productions)))

        initial_symbol = self._grammar.initial_symbol()
        productions = self._grammar.productions()

        text = ""

        if initial_symbol in productions:
            text = transform_production(
                initial_symbol, productions[initial_symbol]) + "\n"

        for non_terminal in sorted(set(productions.keys()) - {initial_symbol}):
            text += transform_production(
                non_terminal, productions[non_terminal]) + "\n"

        self.grammarText.setPlainText(text)

    def _new(self) -> None:
        self._nfa = NFA()
        self._grammar = RegularGrammar()
        self._update_table()

    def _open(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            self._nfa = NFA.load(path)
            self._update_table()

    def _save(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self)
        if path:
            self._nfa.save(path)


def parse_grammar_text(grammar: str) -> RegularGrammar:
    grammar = grammar.strip().replace(" ", "")
    lines = grammar.split("\n")

    if not all(map(GRAMMAR_PATTERN.match, lines)):
        raise RuntimeError("Grammar is not regular")

    initial_symbol, prods = lines[0].split("->")
    productions = {initial_symbol: set(prods.split("|"))}
    for line in lines[1:]:
        non_terminal, prods = line.split("->")
        productions[non_terminal] = set(prods.split("|"))

    return RegularGrammar(initial_symbol, productions)
