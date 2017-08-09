import sys
from ui.main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(600, 400)

        self.addSymbolButton.clicked.connect(self.addSymbol)
        self.addStateButton.clicked.connect(self.addState)

    def addSymbol(self):
        self.transitionTable.insertColumn(self.transitionTable.columnCount())

    def addState(self):
        self.transitionTable.insertRow(self.transitionTable.rowCount())

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
