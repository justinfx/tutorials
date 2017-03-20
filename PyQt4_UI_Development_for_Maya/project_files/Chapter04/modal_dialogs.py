#!/usr/bin/env python

"""
Copyright (c) 2012, Justin Israel (justinisrael@gmail.com) 
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



Chapter04 - Modal vs Non-Modal dialogs

Modal dialog 
	Blocks at the point of calling exec_() until
	the dialog is either closed or the button is pressed

Async dialog 
	Blocks the parent window, but allows code to continue
	running. Response is triggered via a signal when the dialog 
	has finished. 

Non modal 
	Neither blocks the interface, no code execution. 
	Reponse is triggered via signal when dialog has finished. 
"""


from PyQt4 import QtCore, QtGui

class Window(QtGui.QDialog):

	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)
		
		self.resize(300,200)

		self.layout = QtGui.QHBoxLayout(self)

		self.modalButton = QtGui.QRadioButton("Go modal")
		self.asyncModalButton = QtGui.QRadioButton("Go async modal")
		self.nonModalButton = QtGui.QRadioButton("Go non-modal")

		self.layout.addWidget(self.modalButton)
		self.layout.addWidget(self.asyncModalButton)
		self.layout.addWidget(self.nonModalButton)

		self.buttonGroup = QtGui.QButtonGroup()
		self.buttonGroup.setExclusive(True)

		self.buttonGroup.addButton(self.modalButton)
		self.buttonGroup.addButton(self.asyncModalButton)
		self.buttonGroup.addButton(self.nonModalButton)

		# Example of a signal with multiple signatures
		# This one can either return the int id of the button, or the button
		# object itself
		self.buttonGroup.buttonClicked['QAbstractButton*'].connect(self.handle_show_dialog)


	def handle_show_dialog(self, button):
		""" slot to handle a radio button being clicked """

		if button is self.modalButton:
			self.show_modal()

		elif button is self.asyncModalButton:
			self.show_modal_async()

		elif button is self.nonModalButton:
			self.show_non_modal()

		print "Finished running dialog slot"


	def show_modal(self):
		dialog = self._get_dialog()
		ret = dialog.exec_()
		print "Return value from modal dialog was", ret


	def show_modal_async(self):
		dialog = self._get_dialog()
		dialog.setModal(True)
		dialog.show()

		def handle_ret(ret):
			print "Return value from async modal dialog was", ret

		dialog.finished.connect(handle_ret)


	def show_non_modal(self):
		dialog = self._get_dialog()
		dialog.show()

		def handle_ret(ret):
			print "Return value from non-modal dialog was", ret

		dialog.finished.connect(handle_ret)


	def _get_dialog(self):
		""" Private helper method to return a common test dialog """
		dialog = QtGui.QDialog(self)
		dialog.resize(100,100)	
		accept = QtGui.QPushButton("Accept", dialog)
		accept.clicked.connect(dialog.accept)
		return dialog	


if __name__ == "__main__":

	import sys

	app = QtGui.QApplication(sys.argv)

	win = Window()
	win.show()
	win.raise_()

	sys.exit(app.exec_())