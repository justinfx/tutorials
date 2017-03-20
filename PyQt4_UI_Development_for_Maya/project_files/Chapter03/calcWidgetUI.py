# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calcWidget.ui'
#
# Created: Thu Sep  6 12:53:15 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Calculator(object):
    def setupUi(self, Calculator):
        Calculator.setObjectName(_fromUtf8("Calculator"))
        Calculator.resize(461, 104)
        self.verticalLayout = QtGui.QVBoxLayout(Calculator)
        self.verticalLayout.setSpacing(-1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.inputA = QtGui.QLineEdit(Calculator)
        self.inputA.setObjectName(_fromUtf8("inputA"))
        self.horizontalLayout.addWidget(self.inputA)
        self.operatorBox = QtGui.QComboBox(Calculator)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operatorBox.sizePolicy().hasHeightForWidth())
        self.operatorBox.setSizePolicy(sizePolicy)
        self.operatorBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.operatorBox.setObjectName(_fromUtf8("operatorBox"))
        self.operatorBox.addItem(_fromUtf8(""))
        self.operatorBox.addItem(_fromUtf8(""))
        self.operatorBox.addItem(_fromUtf8(""))
        self.operatorBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.operatorBox)
        self.inputB = QtGui.QLineEdit(Calculator)
        self.inputB.setObjectName(_fromUtf8("inputB"))
        self.horizontalLayout.addWidget(self.inputB)
        self.label = QtGui.QLabel(Calculator)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.result = QtGui.QLineEdit(Calculator)
        self.result.setReadOnly(True)
        self.result.setObjectName(_fromUtf8("result"))
        self.horizontalLayout.addWidget(self.result)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(-1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.clearButton = QtGui.QPushButton(Calculator)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout_2.addWidget(self.clearButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Calculator)
        QtCore.QMetaObject.connectSlotsByName(Calculator)

    def retranslateUi(self, Calculator):
        Calculator.setWindowTitle(QtGui.QApplication.translate("Calculator", "Calculator Widget", None, QtGui.QApplication.UnicodeUTF8))
        self.operatorBox.setItemText(0, QtGui.QApplication.translate("Calculator", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.operatorBox.setItemText(1, QtGui.QApplication.translate("Calculator", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.operatorBox.setItemText(2, QtGui.QApplication.translate("Calculator", "/", None, QtGui.QApplication.UnicodeUTF8))
        self.operatorBox.setItemText(3, QtGui.QApplication.translate("Calculator", "*", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Calculator", "=", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("Calculator", "Clear", None, QtGui.QApplication.UnicodeUTF8))

