from ui.main_window_ui import Ui_MainWindow
from automata.dfa import DFA
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QInputDialog)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        self._dfa = DFA(
            set(["q0", "q1"]), set(["a", "b"]), "q0", set(["q1"]),
            {("q0", "a"): "q1", ("q1", "b"): "q0"})

        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(600, 400)

        self.addSymbolButton.clicked.connect(self._addSymbol)
        self.addStateButton.clicked.connect(self._addState)

        self._updateTable()

    def _addSymbol(self) -> None:
        text, ok = QInputDialog.getText(self, "Add symbol", "Symbol:")
        self._dfa.add_symbol(text)
        self._updateTable()

    def _addState(self) -> None:
        text, ok = QInputDialog.getText(self, "Add state", "State:")
        self._dfa.add_state(text)
        self._updateTable()

    def _updateTable(self) -> None:
        states = self._dfa.states()
        alphabet = self._dfa.alphabet()

        self.transitionTable.setRowCount(len(states))
        self.transitionTable.setVerticalHeaderLabels(states)

        self.transitionTable.setColumnCount(len(alphabet))
        self.transitionTable.setHorizontalHeaderLabels(alphabet)

        table = self._dfa.transition_table()
        for i in range(len(states)):
            for j in range(len(alphabet)):
                state = ""
                if (states[i], alphabet[j]) in table:
                    state = table[(states[i], alphabet[j])]
                self.transitionTable.setItem(i, j, QTableWidgetItem(state))
