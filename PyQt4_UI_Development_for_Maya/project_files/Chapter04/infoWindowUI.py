# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infoWindow.ui'
#
# Created: Thu Sep  6 18:13:12 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InfoWindow(object):
    def setupUi(self, InfoWindow):
        InfoWindow.setObjectName(_fromUtf8("InfoWindow"))
        InfoWindow.resize(611, 396)
        self.verticalLayout = QtGui.QVBoxLayout(InfoWindow)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.infoLabel = QtGui.QLabel(InfoWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoLabel.sizePolicy().hasHeightForWidth())
        self.infoLabel.setSizePolicy(sizePolicy)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.verticalLayout.addWidget(self.infoLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.setInfoDumbButton = QtGui.QPushButton(InfoWindow)
        self.setInfoDumbButton.setObjectName(_fromUtf8("setInfoDumbButton"))
        self.horizontalLayout.addWidget(self.setInfoDumbButton)
        self.setInfoSmartButton = QtGui.QPushButton(InfoWindow)
        self.setInfoSmartButton.setObjectName(_fromUtf8("setInfoSmartButton"))
        self.horizontalLayout.addWidget(self.setInfoSmartButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(InfoWindow)
        QtCore.QMetaObject.connectSlotsByName(InfoWindow)

    def retranslateUi(self, InfoWindow):
        InfoWindow.setWindowTitle(QtGui.QApplication.translate("InfoWindow", "Info About You", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("InfoWindow", "[Info About You]", None, QtGui.QApplication.UnicodeUTF8))
        self.setInfoDumbButton.setText(QtGui.QApplication.translate("InfoWindow", "Set with Dumb Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.setInfoSmartButton.setText(QtGui.QApplication.translate("InfoWindow", "Set with Smart Dialog", None, QtGui.QApplication.UnicodeUTF8))

