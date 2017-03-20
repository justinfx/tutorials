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



blocking.py 

Chapter03 - Blocking the UI

An example of how one should avoid blocking the main 
GUI thread, and make use of signal/slot notifications.
"""

import sys
import subprocess

from PyQt4 import QtCore, QtGui

## adjust the sleep shell command for windows platform
import platform 
if platform.system() == "Windows":
	SLEEP_CMD = ['python', '-c', 'import time\ntime.sleep(5)']
else:
	SLEEP_CMD = ['sleep', '5']

class BlockingTest(object):

	def main(self):

		app = QtGui.QApplication(sys.argv)

		self.win = QtGui.QWidget()
		self.win.resize(300,200)

		layout = QtGui.QVBoxLayout(self.win)

		blocking_button = QtGui.QPushButton("Block")
		blocking_button.clicked.connect(self.blocking)
		layout.addWidget(blocking_button)

		signal_button = QtGui.QPushButton("Signals")
		signal_button.clicked.connect(self.non_blocking)
		layout.addWidget(signal_button)

		self.output = QtGui.QLineEdit()
		layout.addWidget(self.output)

		clear_button = QtGui.QPushButton("Clear")
		clear_button.clicked.connect(self.output.clear)
		layout.addWidget(clear_button)

		self.win.show()
		self.win.raise_()

		app.exec_()


	def finished(self, returnCode):
		self.setMessage("Return code: %s" % returnCode)


	def setMessage(self, msg):
		print msg
		self.output.setText(msg)		


	def blocking(self):
		self.setMessage("Starting blocking sleep")

		# process = subprocess.Popen(['sleep', '5'])
		process = subprocess.Popen(SLEEP_CMD)
		ret = process.wait()
		self.finished(ret)


	def non_blocking(self):
		self.setMessage("Starting non blocking sleep")

		process = QtCore.QProcess(parent=self.win)
		process.setProcessChannelMode(process.ForwardedChannels)
		process.finished.connect(self.finished)
		# process.start('sleep', ['5'])
		process.start(SLEEP_CMD[0], SLEEP_CMD[1:])


if __name__ == "__main__":
	app = BlockingTest()
	app.main()

