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
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.regexLabel = QtWidgets.QLabel(self.centralwidget)
        self.regexLabel.setObjectName("regexLabel")
        self.horizontalLayout_1.addWidget(self.regexLabel)
        self.regexInput = QtWidgets.QLineEdit(self.centralwidget)
        self.regexInput.setObjectName("regexInput")
        self.horizontalLayout_1.addWidget(self.regexInput)
        self.verticalLayout_2.addLayout(self.horizontalLayout_1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.FALabel = QtWidgets.QLabel(self.centralwidget)
        self.FALabel.setObjectName("FALabel")
        self.verticalLayout.addWidget(self.FALabel)
        self.transitionTable = QtWidgets.QTableWidget(self.centralwidget)
        self.transitionTable.setRowCount(0)
        self.transitionTable.setColumnCount(0)
        self.transitionTable.setObjectName("transitionTable")
        self.verticalLayout.addWidget(self.transitionTable)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addSymbolButton = QtWidgets.QPushButton(self.centralwidget)
        self.addSymbolButton.setObjectName("addSymbolButton")
        self.horizontalLayout.addWidget(self.addSymbolButton)
        self.removeSymbolButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeSymbolButton.setObjectName("removeSymbolButton")
        self.horizontalLayout.addWidget(self.removeSymbolButton)
        self.addStateButton = QtWidgets.QPushButton(self.centralwidget)
        self.addStateButton.setObjectName("addStateButton")
        self.horizontalLayout.addWidget(self.addStateButton)
        self.removeStateButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeStateButton.setObjectName("removeStateButton")
        self.horizontalLayout.addWidget(self.removeStateButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Automata Editor"))
        self.regexLabel.setText(_translate("MainWindow", "Regular Expression:"))
        self.FALabel.setText(_translate("MainWindow", "Automaton transition table"))
        self.addSymbolButton.setText(_translate("MainWindow", "Add Symbol"))
        self.removeSymbolButton.setText(_translate("MainWindow", "Remove Symbol"))
        self.addStateButton.setText(_translate("MainWindow", "Add State"))
        self.removeStateButton.setText(_translate("MainWindow", "Remove State"))

