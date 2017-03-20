# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calculator.ui'
#
# Created: Thu Sep  6 14:50:45 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CalculatorWindow(object):
    def setupUi(self, CalculatorWindow):
        CalculatorWindow.setObjectName(_fromUtf8("CalculatorWindow"))
        CalculatorWindow.resize(450, 140)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CalculatorWindow.sizePolicy().hasHeightForWidth())
        CalculatorWindow.setSizePolicy(sizePolicy)
        CalculatorWindow.setMinimumSize(QtCore.QSize(0, 140))
        CalculatorWindow.setMaximumSize(QtCore.QSize(16777215, 140))
        self.centralwidget = QtGui.QWidget(CalculatorWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        CalculatorWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(CalculatorWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        CalculatorWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(CalculatorWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        CalculatorWindow.setStatusBar(self.statusbar)
        self.actionClear = QtGui.QAction(CalculatorWindow)
        self.actionClear.setObjectName(_fromUtf8("actionClear"))
        self.menuFile.addAction(self.actionClear)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(CalculatorWindow)
        QtCore.QMetaObject.connectSlotsByName(CalculatorWindow)

    def retranslateUi(self, CalculatorWindow):
        CalculatorWindow.setWindowTitle(QtGui.QApplication.translate("CalculatorWindow", "Calculator", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("CalculatorWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setText(QtGui.QApplication.translate("CalculatorWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))

