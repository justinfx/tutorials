
"""
Copyright (c) 2011, Justin Israel (justinisrael@gmail.com) 
All rights reserved. 

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met: 

 * Redistributions of source code must retain the above copyright notice, 
   this list of conditions and the following disclaimer. 
 * Redistributions in binary form must reproduce the above copyright 
   notice, this list of conditions and the following disclaimer in the 
   documentation and/or other materials provided with the distribution. 
 * Neither the name of cmiVFX.com nor the names of its contributors may be 
   used to endorse or promote products derived from this software without 
   specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE. 



assetImporterWin.py

Alternate UI example using a QtDesigner UI and PyQt4

"""

from functools import partial

from AssetImporter.assetImporter4 import *

from PyQt4 import QtCore, QtGui

# our UI modules have been moved to a package directory
# right under the current location of this script.
# We also added the flowlayout.py module that was shipped
# with PyQt4 installation, in the examples directory.
from ui.AssetImporterUI import Ui_AssetImporterWindow
from ui.flowlayout import FlowLayout

# this module has UI utility functions that we  need
import maya.OpenMayaUI as mui
import sip

# we use a global app variable and get an INSTANCE
# of the QApplication. There can be only one, so all
# windows need to share it, and not try to create another.
global app
app = QtGui.QApplication.instance()


class AssetImporterWin(QtGui.QDialog, Ui_AssetImporterWindow):
    """
    AssetImporterWin(QtGui.QDialog, Ui_AssetImporterWindow)

        A QDialog using PyQt4.
        Provides an interface to the AssetImporter module.
    """

    def __init__(self, parent=None):
        
        # we need to make sure to call the __init__() method
        # on the super class, when we overload existing methods
        super(AssetImporterWin, self).__init__(parent=parent)


        # access to the AssetImporter tool itself
        self.importer = AssetImporter()
        self._objectList = []
        self._iconSize  = (128,128)

        # Since we also subclassed Ui_AssetImporterWindow, we got
        # the setupUi() method which configures this dialog with
        # our setup from the QtDesigner file
        self.setupUi(self)

        self.splitter.setSizes([500, 300])

        # A FlowLayout, imported from the examples directory
        # bundled with PyQt4 installation
        self.libraryLayout = FlowLayout(self.libraryScroll)


        # lets make the first entry an empty string meaning All Shows
        self.showBox.clear()
        self.showBox.addItem("")        
        for show in self.importer.listShows():
            self.showBox.addItem(show)


        # connections
        # This is the new way to make SIGNAL -> SLOT connections
        # Its much cleaner and easier to use. The event points to the
        # handler function that should be called.
        self.reloadLibButton.clicked.connect(self.refreshAssets)
        self.reloadImportedButton.clicked.connect(self.refreshImported)
        self.importedList.itemClicked.connect(self.importedItemSelected)
        self.showBox.currentIndexChanged.connect(self.refreshAssets)



    # We are leaving this method using *args so that it can be 
    # a SLOT for multiple signals, with different return parameters
    def refreshAssets(self, *args):
        """
        refreshAssets(*args)
            
            A callback command that refreshes the list of available
            assets ready for import. 
            The "Refresh Library" button calls this when clicked.
        """

        # clear out any previous children of the grid layout
        while not self.libraryLayout.isEmpty():
            item = self.libraryLayout.takeAt(0)
            item.widget().destroy()
        

        currentShow = str(self.showBox.currentText())
        if currentShow:
            self.importer.show = currentShow
            allshows = False
        else:
            allshows = True

        for asset in self.importer.list(allShows=allshows):

            # this is an example of a callback using the functools
            # module. Its a way to package up a method and arguments
            # so that maya can call it later, such as by just calling:  cmd()
            # We imported this as:   from functools import partial
            cmd = partial(self.importer.load, asset)

            # We are using our custom widget AssetItem (defined below)
            item = AssetItem(size = self._iconSize, imagePath = asset.image)
            item.setText('%s \n(%s)' % (asset.name, asset.show))
            
            # create a connection on the fly
            item.button.clicked.connect(cmd)

            self.libraryLayout.addWidget(item)


    def refreshImported(self):
        """
        refreshImported()

            A callback command the refreshes the list of already
            imported assets in the scene. 
            The "Refresh Imported" button calls this when clicked.
        """
        
        self.importedList.clear()

        for item in self.importer.findImported():

            listItem = QtGui.QListWidgetItem()
            listItem.setText(item[0])

            # in python, we can add arbitrary attributes onto these
            # objects for storage, unless of course the class specifically
            # prevents it. If you had a lot more custom stuff to store
            # and process, you would probably want to subclass your own
            # custom ListWidgetItem. But for now, we can just store
            # the Asset on the List item. We will be able to get this
            # back when we look up list items later.
            listItem.asset = item[1]

            self.importedList.addItem(listItem)
    

    def importedItemSelected(self, item):
        """
        importedItemSelected(QtGui.QListWidgetItem item)

            A callback command that selects the object in the scene
            when the corresponding item is selected in the list
            of imported assets.
        """

        node = str(item.text())

        if cmds.objExists(node):
        
            cmds.select(node, r=True)
            
            # Since we stored the Asset object with each list item
            # we now have access to it and could do something with it
            # such as offering to swap out assets, etc.
            # Lets just print it.
            print "Asset was just selected:"
            print item.asset
       
        
                               
def getMayaWindow():
    """
    getMayaWindow()
        A helper function that finds the maya mainWindow
        and returns a proper PyQt4 QMainWindow object for
        us to reference.
    """
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)


def show():
    """
    show() -> AssetImporterWin
        
        A convenience function for showing the User Interface.
    """

    # if we didn't parent the AssetImporter to the maya mainWindow,
    # then it would pop up in the center of the screen as opposed to
    # the center of the maya app, and would NOT be a child window.
    # Things like docking probably would not work if it were not a child.
    i = AssetImporterWin(parent=getMayaWindow())
    i.show()

    return i


class AssetItem(QtGui.QWidget):
    """
    AssetItem (QtGui.QWidget)

        A custom widget for displaying an Asset.
        Contains a picture that acts like a button,
        along with a text description.
    """

    def __init__(self, text='', imagePath='', size=None, parent=None):
        super(AssetItem, self).__init__(parent=parent)

        self.layout = QtGui.QVBoxLayout(self)
        self.button = QtGui.QPushButton()
        self.text   = QtGui.QLabel()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.text)

        if text:
            self.setText(text)
        
        if imagePath:
            self.setImage(imagePath)

        if size:
            self.setSize(size)
        else:
            set.setSize(64, 64)
    
    def setText(self, txt):
        self.text.setText(txt)
    
    def setImage(self, imagePath):
        self.button.setIcon(QtGui.QIcon(imagePath))
    
    def setSize(self, size):
        size = QtCore.QSize(size[0], size[1])
        self.button.setFixedSize(size)
        self.button.setIconSize(size)


