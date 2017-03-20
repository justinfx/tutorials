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


coordinates.py 

Chapter03 - QWidget Coordinate Space

A QWidget window containing color-coded child widget areas. 
A QPushButton that, when clicked, will cycle through different 
parents. Demonstrates coordinate space being relative to the parent. 

"""

from PyQt4 import QtCore, QtGui
from random import randint

from collections import deque

class Widget(QtGui.QWidget):

    def __init__(self):
        super(Widget, self).__init__()

        self.setObjectName("MainWindow")

        mainLayout = QtGui.QVBoxLayout(self)
        mainLayout.setSpacing(0)
        mainLayout.setMargin(20)

        self.feedback = QtGui.QLabel()
        self.feedback.setFixedHeight(50)
        mainLayout.addWidget(self.feedback)

        self.widgets = deque()
        self.widgets.append(None)
        self.widgets.append(self)

        for i, color in enumerate(('red', 'green', 'blue')): 
            w = QtGui.QWidget()
            name = "widget%d" % i
            w.setObjectName(name)
            w.setStyleSheet("#%s { background: %s }" % (name, color))
            mainLayout.addWidget(w)
            self.widgets.append(w)

        self.button = QtGui.QPushButton("Move", self)
        self.button.clicked.connect(self.random_move)

    def random_move(self):
        b = self.button
        parent = b.parent()
        pos = b.pos()
        name = parent and parent.objectName() or "None"

        old_str = "Old Parent/Pos:\t%s %s" % (name, (pos.x(), pos.y()))

        new_parent = parent 
        while new_parent is parent:
            self.widgets.rotate(-1)
            new_parent = self.widgets[0]

        self.button.setParent(new_parent)

        if new_parent is None:
        	min_pos = self.pos()
        	max_pos = self.geometry().bottomRight()
        	self.button.move(
        		randint(min_pos.x(), max_pos.x()), 
        		randint(min_pos.y(), max_pos.y())
        		)
        else:
        	self.button.move(randint(0, 300), randint(0, 75))

        pos = b.pos()
        name = new_parent and new_parent.objectName() or "None"
        new_str = "New Parent/Pos:\t%s %s" % (name, (pos.x(), pos.y()))

        self.feedback.setText('%s\n%s' % (old_str, new_str))

        self.button.show()

if __name__ == "__main__":

    app = QtGui.QApplication([])

    w = Widget()
    w.resize(600,500)
    w.show()
    w.raise_()

    app.exec_()
    