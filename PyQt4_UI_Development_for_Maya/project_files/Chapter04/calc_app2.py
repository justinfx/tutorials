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


Chapter04 - Calculator App #2

This second version shows how to create custom QWidget 
subclasses, also inheriting from the UI classes. 
"""

from PyQt4 import QtCore, QtGui

from calculatorWinUI import Ui_CalculatorWindow
from calcWidgetUI import Ui_Calculator

import operator

class Window(QtGui.QMainWindow, Ui_CalculatorWindow):

	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)
		
		# Multiple-inheritence approach: http://goo.gl/L7H9X
		# Window class inherits from both QMainWindow and the 
		# Ui_CalculatorWindow class from designer.
		# All members from the Ui class are directly located
		# on `self`
		self.setupUi(self)

		self.calcWidget = Calculator()
		self.setCentralWidget(self.calcWidget)

		self.actionClear.triggered.connect(self.calcWidget.clear)


class Calculator(QtGui.QWidget):

	OPS = {
		'+': operator.add,
		'-': operator.sub,
		'/': operator.div,
		'*': operator.mul,
	}

	def __init__(self, *args, **kwargs):
		super(Calculator, self).__init__(*args, **kwargs)

		# Single-inheritence approach: http://goo.gl/WNiHc
		# Calculator class only inherits from QWidget
		# A specific member attribute self.ui contains all
		# widgets set up in the designer.		
		self.ui = Ui_Calculator()
		self.ui.setupUi(self)

		self.ui.calcButton = QtGui.QPushButton("Calculate")
		self.ui.horizontalLayout_2.addWidget(self.ui.calcButton)

		# Create a validator for each QLineEdit that only
		# allows a user to enter floats: 123.123
		self.ui.inputA.setValidator(QtGui.QDoubleValidator())
		self.ui.inputB.setValidator(QtGui.QDoubleValidator())

		# instead of using the stock operator values set in the
		# ui file, lets set the box to match our class attribute
		self.ui.operatorBox.clear()
		self.ui.operatorBox.addItems(self.OPS.keys())

		self.ui.clearButton.clicked.connect(self.clear)
		self.ui.calcButton.clicked.connect(self.calc)


	def clear(self):
		""" Slot to clear the form fields """

		self.ui.inputA.clear()
		self.ui.inputB.clear()
		self.ui.result.clear()

	def calc(self):
		""" Calculate the result from the form values """

		op_str = str(self.ui.operatorBox.currentText())
		op = self.OPS.get(op_str)
		if not op:
			return

		inputA = self.ui.inputA.text()
		inputB = self.ui.inputB.text()

		# just silently return if either field is empty
		if not (inputA and inputB):
			return

		try:
			i1 = float(inputA)
			i2 = float(inputB)
			result = op(i1, i2)

		except Exception, e:
			# inform the user if the operation results in
			# an error. Such as dividing by zero.
			QtGui.QMessageBox.warning(self, 
				"Could not calculate results",
				"Reason:\n%s" % e)
		else:
			self.ui.result.setText(str(result))
		


if __name__ == "__main__":

	import sys

	app = QtGui.QApplication(sys.argv)

	win = Window()
	win.show()
	win.raise_()

	sys.exit(app.exec_())