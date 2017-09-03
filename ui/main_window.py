from ui.main_window_ui import Ui_MainWindow
from automata.nfa import NFA
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QInputDialog, QMessageBox)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        self._dfa = NFA(
            set(["q0", "q1"]), set(["a", "b"]), "q0", set(["q1"]),
            {("q0", "a"): {"q1"}, ("q1", "b"): {"q0"}})

        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(600, 400)

        self.addSymbolButton.clicked.connect(self._add_symbol)
        self.addStateButton.clicked.connect(self._add_state)
        self.removeSymbolButton.clicked.connect(self._remove_symbol)
        self.removeStateButton.clicked.connect(self._remove_state)

        self._update_table()
        self.transitionTable.cellChanged.connect(self._update_dfa)

    def _add_symbol(self) -> None:
        text, _ = QInputDialog.getText(self, "Add symbol", "Symbol:")
        self._dfa.add_symbol(text)
        self._update_table()

    def _add_state(self) -> None:
        text, _ = QInputDialog.getText(self, "Add state", "State:")
        self._dfa.add_state(text)
        self._update_table()

    def _remove_symbol(self) -> None:
        text, _ = QInputDialog.getText(self, "Remove symbol", "Symbol:")
        self._dfa.remove_symbol(text)
        self._update_table()

    def _remove_state(self) -> None:
        text, _ = QInputDialog.getText(self, "Remove state", "State:")
        self._dfa.remove_state(text)
        self._update_table()

    def _update_dfa(self, row: int, col: int) -> None:
        states = self._dfa.states()
        alphabet = self._dfa.alphabet()
        next_states = \
            set(self.transitionTable.item(row, col).text().split(","))

        if next_states != {""}:
            try:
                self._dfa.set_transition(
                    states[row], alphabet[col], next_states)
            except KeyError as error:
                QMessageBox.information(self, "Error", error.args[0])
                self.transitionTable.item(row, col).setText("")

    def _update_table(self) -> None:
        states = self._dfa.states()
        alphabet = self._dfa.alphabet()

        self.transitionTable.setRowCount(len(states))
        self.transitionTable.setVerticalHeaderLabels(states)

        self.transitionTable.setColumnCount(len(alphabet))
        self.transitionTable.setHorizontalHeaderLabels(alphabet)

        table = self._dfa.transition_table()
        for i, state in enumerate(states):
            for j, symbol in enumerate(alphabet):
                transition = ",".join(table[(state, symbol)]) \
                    if (state, symbol) in table else ""
                self.transitionTable.setItem(
                    i, j, QTableWidgetItem(transition))
