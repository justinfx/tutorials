# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infoDialog.ui'
#
# Created: Thu Sep  6 17:55:23 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InfoDialog(object):
    def setupUi(self, InfoDialog):
        InfoDialog.setObjectName(_fromUtf8("InfoDialog"))
        InfoDialog.resize(281, 225)
        self.verticalLayout = QtGui.QVBoxLayout(InfoDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(InfoDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.firstName = QtGui.QLineEdit(InfoDialog)
        self.firstName.setObjectName(_fromUtf8("firstName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.firstName)
        self.label_2 = QtGui.QLabel(InfoDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lastName = QtGui.QLineEdit(InfoDialog)
        self.lastName.setObjectName(_fromUtf8("lastName"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lastName)
        self.label_3 = QtGui.QLabel(InfoDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.email = QtGui.QLineEdit(InfoDialog)
        self.email.setObjectName(_fromUtf8("email"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.email)
        self.label_4 = QtGui.QLabel(InfoDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.age = QtGui.QSpinBox(InfoDialog)
        self.age.setMinimum(1)
        self.age.setObjectName(_fromUtf8("age"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.age)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(InfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(InfoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InfoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InfoDialog)

    def retranslateUi(self, InfoDialog):
        InfoDialog.setWindowTitle(QtGui.QApplication.translate("InfoDialog", "Enter Profile Info", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("InfoDialog", "First Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("InfoDialog", "Last Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("InfoDialog", "Email", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("InfoDialog", "Age", None, QtGui.QApplication.UnicodeUTF8))

