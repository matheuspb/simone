from typing import Set
import re
from ui.main_window_ui import Ui_MainWindow
from tools.nfa import NFA
from tools.grammar import RegularGrammar
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QInputDialog, QMessageBox, QFileDialog)

GRAMMAR_PATTERN = re.compile(r"^[A-Z]'?->[a-z&][A-Z]?(\|[a-z&][A-Z]?)*$")


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.setFixedSize(600, 400)

        self.addSymbolButton.clicked.connect(self._add_symbol)
        self.addStateButton.clicked.connect(self._add_state)
        self.removeSymbolButton.clicked.connect(self._remove_symbol)
        self.removeStateButton.clicked.connect(self._remove_state)
        self.finalStateButton.clicked.connect(self._toggle_final_state)

        self.fromNFAbutton.clicked.connect(self._nfa_to_grammar)
        self.toNFAbutton.clicked.connect(self._grammar_to_nfa)

        self.testButton.clicked.connect(self._test_string)

        self.actionNew.triggered.connect(self._new)
        self.actionOpen.triggered.connect(self._open)
        self.actionSave.triggered.connect(self._save)

        self.transitionTable.cellChanged.connect(self._update_nfa)

        self._grammar = RegularGrammar()
        self._nfa = NFA()
        self._update_table()

    def _add_symbol(self) -> None:
        text, ok = QInputDialog.getText(self, "Add symbol", "Symbol:")
        if ok:
            self._nfa.add_symbol(text)
            self._update_table()

    def _add_state(self) -> None:
        text, ok = QInputDialog.getText(self, "Add state", "State:")
        if ok:
            self._nfa.add_state(text)
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
        text, ok = QInputDialog.getText(
            self, "Final state", "State:")
        if ok:
            self._nfa.toggle_final_state(text)
            self._update_table()

    def _test_string(self) -> None:
        try:
            self.statusbar.showMessage(
                "String accepted" if self._nfa.accept(self.inputString.text())
                else "String rejected")
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

    def _update_nfa(self, row: int, col: int) -> None:
        states = self._nfa.states()
        alphabet = self._nfa.alphabet()
        next_states = \
            set(self.transitionTable.item(row, col).text().split(","))

        try:
            self._nfa.set_transition(
                states[row], alphabet[col],
                next_states if next_states != {""} else set())
        except KeyError as error:
            QMessageBox.information(self, "Error", error.args[0])
            self.transitionTable.item(row, col).setText("")

    def _update_table(self) -> None:
        states = []
        for state in self._nfa.states():
            preffix = ""
            if state in self._nfa.final_states():
                preffix += "*"
            if state == self._nfa.initial_state():
                preffix += "->"
            states.append(preffix + state)

        alphabet = self._nfa.alphabet()

        self.transitionTable.setRowCount(len(states))
        self.transitionTable.setVerticalHeaderLabels(states)

        self.transitionTable.setColumnCount(len(alphabet))
        self.transitionTable.setHorizontalHeaderLabels(alphabet)

        table = self._nfa.transition_table()
        for i, state in enumerate(self._nfa.states()):
            for j, symbol in enumerate(alphabet):
                transition = ",".join(table[(state, symbol)]) \
                    if (state, symbol) in table else ""
                self.transitionTable.setItem(
                    i, j, QTableWidgetItem(transition))

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
