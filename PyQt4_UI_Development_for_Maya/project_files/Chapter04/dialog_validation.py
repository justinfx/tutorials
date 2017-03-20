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


Chapter04 - dialog_validation.py

Using custom dialogs

"""


from PyQt4 import QtCore, QtGui

from infoDialogUI import Ui_InfoDialog
from infoWindowUI import Ui_InfoWindow



class InfoWindow(QtGui.QDialog, Ui_InfoWindow):

	def __init__(self, *args, **kwargs):
		super(InfoWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)

		# the default slot will use the DumbInfoDialog
		self.setInfoDumbButton.clicked.connect(self.show_dumb_dialog)
		self.setInfoSmartButton.clicked.connect(self.show_smart_dialog)


	def show_smart_dialog(self):
		dialog = SmartInfoDialog(self)

		if dialog.exec_() == dialog.Accepted:
			self.process_dialog(dialog)


	def show_dumb_dialog(self):
		dialog = DumbInfoDialog(self)

		while True:
			if dialog.exec_() == dialog.Accepted:

				first 	= dialog.firstName.text()
				last 	= dialog.lastName.text()
				email 	= dialog.email.text()	

				if not (first and last and email):
					err = "All fields are required"
					QtGui.QMessageBox.warning(self, "Error in form", err)
					continue

				self.process_dialog(dialog)

			break


	def process_dialog(self, dialog):
		""" Process a dialog widget as-is and update display """

		first 	= dialog.firstName.text()
		last 	= dialog.lastName.text()
		email 	= dialog.email.text()	
		age 	= dialog.age.value()

		plural 	= (age > 1) and "s" or ""
		
		msg = """
			Hi, %(first)s %(last)s! <br>
			Your E-Mail Address is %(email)s <br>
			And you are %(age)d year%(plural)s old!   
		""" % locals()

		self.infoLabel.setText(msg)


class DumbInfoDialog(QtGui.QDialog, Ui_InfoDialog):
	"""
	A simple dialog widget with no logic
	"""
	def __init__(self, parent=None):
		super(DumbInfoDialog, self).__init__(parent)
		self.setupUi(self)


class SmartInfoDialog(DumbInfoDialog):
	"""
	Subclass of DumbInfoDialog 
	Adds field validators, and form validation during the 
	accept action. 
	"""
	def __init__(self, parent=None):
		super(SmartInfoDialog, self).__init__(parent)

		# Weak email validation regex: http://www.regular-expressions.info/email.html
		self._email_rx = QtCore.QRegExp(
			r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$', 
			QtCore.Qt.CaseInsensitive)

		self.email.setValidator(QtGui.QRegExpValidator(self._email_rx ))


	def accept(self):
		err = ""

		if not (self.firstName.text() and self.lastName.text()):
			err = "First and Last name fields are required"

		elif not self._email_rx.exactMatch(self.email.text()):
			err = "Email address is not valid"

		if err:
			QtGui.QMessageBox.warning(self, "Error in form", err)
			return

		super(SmartInfoDialog, self).accept()



if __name__ == "__main__":

	import sys

	app = QtGui.QApplication(sys.argv)

	win = InfoWindow()
	win.show()
	win.raise_()

	sys.exit(app.exec_())