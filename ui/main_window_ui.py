# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.regexLabel = QtWidgets.QLabel(self.centralwidget)
        self.regexLabel.setObjectName("regexLabel")
        self.horizontalLayout_1.addWidget(self.regexLabel)
        self.regexInput = QtWidgets.QLineEdit(self.centralwidget)
        self.regexInput.setObjectName("regexInput")
        self.horizontalLayout_1.addWidget(self.regexInput)
        self.verticalLayout_3.addLayout(self.horizontalLayout_1)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.automatonTab = QtWidgets.QWidget()
        self.automatonTab.setObjectName("automatonTab")
        self.gridLayout = QtWidgets.QGridLayout(self.automatonTab)
        self.gridLayout.setObjectName("gridLayout")
        self.transitionTable = QtWidgets.QTableWidget(self.automatonTab)
        self.transitionTable.setRowCount(0)
        self.transitionTable.setColumnCount(0)
        self.transitionTable.setObjectName("transitionTable")
        self.gridLayout.addWidget(self.transitionTable, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.addSymbolButton = QtWidgets.QPushButton(self.automatonTab)
        self.addSymbolButton.setObjectName("addSymbolButton")
        self.verticalLayout_2.addWidget(self.addSymbolButton)
        self.addStateButton = QtWidgets.QPushButton(self.automatonTab)
        self.addStateButton.setObjectName("addStateButton")
        self.verticalLayout_2.addWidget(self.addStateButton)
        self.removeSymbolButton = QtWidgets.QPushButton(self.automatonTab)
        self.removeSymbolButton.setObjectName("removeSymbolButton")
        self.verticalLayout_2.addWidget(self.removeSymbolButton)
        self.removeStateButton = QtWidgets.QPushButton(self.automatonTab)
        self.removeStateButton.setObjectName("removeStateButton")
        self.verticalLayout_2.addWidget(self.removeStateButton)
        self.finalStateButton = QtWidgets.QPushButton(self.automatonTab)
        self.finalStateButton.setObjectName("finalStateButton")
        self.verticalLayout_2.addWidget(self.finalStateButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.tabWidget.addTab(self.automatonTab, "")
        self.grammarTab = QtWidgets.QWidget()
        self.grammarTab.setObjectName("grammarTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.grammarTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.grammarText = QtWidgets.QPlainTextEdit(self.grammarTab)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(10)
        self.grammarText.setFont(font)
        self.grammarText.setObjectName("grammarText")
        self.gridLayout_2.addWidget(self.grammarText, 0, 0, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.fromNFAbutton = QtWidgets.QPushButton(self.grammarTab)
        self.fromNFAbutton.setObjectName("fromNFAbutton")
        self.verticalLayout_6.addWidget(self.fromNFAbutton)
        self.toNFAbutton = QtWidgets.QPushButton(self.grammarTab)
        self.toNFAbutton.setObjectName("toNFAbutton")
        self.verticalLayout_6.addWidget(self.toNFAbutton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.verticalLayout_6, 0, 1, 1, 1)
        self.tabWidget.addTab(self.grammarTab, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout_1.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputString = QtWidgets.QLineEdit(self.centralwidget)
        self.inputString.setObjectName("inputString")
        self.horizontalLayout.addWidget(self.inputString)
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setObjectName("testButton")
        self.horizontalLayout.addWidget(self.testButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuMinimize = QtWidgets.QMenu(self.menubar)
        self.menuMinimize.setObjectName("menuMinimize")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionRemove_unreachable_states = QtWidgets.QAction(MainWindow)
        self.actionRemove_unreachable_states.setObjectName("actionRemove_unreachable_states")
        self.actionRemove_dead_states = QtWidgets.QAction(MainWindow)
        self.actionRemove_dead_states.setObjectName("actionRemove_dead_states")
        self.actionMerge_equivalent_states = QtWidgets.QAction(MainWindow)
        self.actionMerge_equivalent_states.setObjectName("actionMerge_equivalent_states")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuMinimize.addAction(self.actionRemove_unreachable_states)
        self.menuMinimize.addAction(self.actionRemove_dead_states)
        self.menuMinimize.addAction(self.actionMerge_equivalent_states)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMinimize.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Automata Editor"))
        self.regexLabel.setText(_translate("MainWindow", "Regular Expression:"))
        self.addSymbolButton.setText(_translate("MainWindow", "Add Symbol"))
        self.addStateButton.setText(_translate("MainWindow", "Add State"))
        self.removeSymbolButton.setText(_translate("MainWindow", "Remove Symbol"))
        self.removeStateButton.setText(_translate("MainWindow", "Remove State"))
        self.finalStateButton.setText(_translate("MainWindow", "Toggle final state"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.automatonTab), _translate("MainWindow", "Automaton"))
        self.fromNFAbutton.setText(_translate("MainWindow", "Convert from NFA"))
        self.toNFAbutton.setText(_translate("MainWindow", "Convert to NFA"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.grammarTab), _translate("MainWindow", "Grammar"))
        self.testButton.setText(_translate("MainWindow", "Test string"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuMinimize.setTitle(_translate("MainWindow", "Transformations"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionRemove_unreachable_states.setText(_translate("MainWindow", "Remove unreachable states"))
        self.actionRemove_dead_states.setText(_translate("MainWindow", "Remove dead states"))
        self.actionMerge_equivalent_states.setText(_translate("MainWindow", "Merge equivalent states"))

