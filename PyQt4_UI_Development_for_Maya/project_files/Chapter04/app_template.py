#!/usr/bin/env python

"""
Chapter04 - App Template

A common structure for the entry-point into a 
new PyQt4 application
"""


from PyQt4 import QtCore, QtGui

class Window(QtGui.QDialog):

	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)
		
		# custom code here
		self.resize(800,600)


if __name__ == "__main__":

	import sys

	app = QtGui.QApplication(sys.argv)

	win = Window()
	win.show()
	win.raise_()

	sys.exit(app.exec_())