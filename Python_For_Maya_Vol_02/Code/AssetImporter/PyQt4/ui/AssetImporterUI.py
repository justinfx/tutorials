# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/justin/Desktop/Python_for_Maya_vol2/Code/AssetImporter/PyQt4/ui/AssetImporterUI.ui'
#
# Created: Wed Nov  9 20:31:42 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AssetImporterWindow(object):
    def setupUi(self, AssetImporterWindow):
        AssetImporterWindow.setObjectName(_fromUtf8("AssetImporterWindow"))
        AssetImporterWindow.resize(1019, 607)
        AssetImporterWindow.setWindowTitle(QtGui.QApplication.translate("AssetImporterWindow", "AssetImporter PyQT4", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(AssetImporterWindow)
        self.horizontalLayout_3.setMargin(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.splitter = QtGui.QSplitter(AssetImporterWindow)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.groupBox = QtGui.QGroupBox(self.splitter)
        self.groupBox.setTitle(QtGui.QApplication.translate("AssetImporterWindow", "Library", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setMargin(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.reloadLibButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reloadLibButton.sizePolicy().hasHeightForWidth())
        self.reloadLibButton.setSizePolicy(sizePolicy)
        self.reloadLibButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.reloadLibButton.setText(QtGui.QApplication.translate("AssetImporterWindow", "Refresh Library", None, QtGui.QApplication.UnicodeUTF8))
        self.reloadLibButton.setObjectName(_fromUtf8("reloadLibButton"))
        self.horizontalLayout_2.addWidget(self.reloadLibButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setText(QtGui.QApplication.translate("AssetImporterWindow", "Show: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.showBox = QtGui.QComboBox(self.groupBox)
        self.showBox.setObjectName(_fromUtf8("showBox"))
        self.showBox.addItem(_fromUtf8(""))
        self.showBox.setItemText(0, QtGui.QApplication.translate("AssetImporterWindow", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout_2.addWidget(self.showBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.libraryFrame = QtGui.QScrollArea(self.groupBox)
        self.libraryFrame.setWidgetResizable(True)
        self.libraryFrame.setObjectName(_fromUtf8("libraryFrame"))
        self.libraryScroll = QtGui.QWidget()
        self.libraryScroll.setGeometry(QtCore.QRect(0, 0, 583, 520))
        self.libraryScroll.setObjectName(_fromUtf8("libraryScroll"))
        self.libraryFrame.setWidget(self.libraryScroll)
        self.verticalLayout_2.addWidget(self.libraryFrame)
        self.groupBox_2 = QtGui.QGroupBox(self.splitter)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("AssetImporterWindow", "Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setMargin(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.reloadImportedButton = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reloadImportedButton.sizePolicy().hasHeightForWidth())
        self.reloadImportedButton.setSizePolicy(sizePolicy)
        self.reloadImportedButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.reloadImportedButton.setText(QtGui.QApplication.translate("AssetImporterWindow", "Refresh Imported", None, QtGui.QApplication.UnicodeUTF8))
        self.reloadImportedButton.setObjectName(_fromUtf8("reloadImportedButton"))
        self.horizontalLayout.addWidget(self.reloadImportedButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.importedList = QtGui.QListWidget(self.groupBox_2)
        self.importedList.setObjectName(_fromUtf8("importedList"))
        self.verticalLayout.addWidget(self.importedList)
        self.horizontalLayout_3.addWidget(self.splitter)

        self.retranslateUi(AssetImporterWindow)
        QtCore.QMetaObject.connectSlotsByName(AssetImporterWindow)

    def retranslateUi(self, AssetImporterWindow):
        pass

