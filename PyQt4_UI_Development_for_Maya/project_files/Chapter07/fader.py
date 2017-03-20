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


fader.py

Chapter07 

A widget with a custom paintEvent, allowing 
one widget to be faded into another widget.
"""

from PyQt4 import QtCore, QtGui


class FaderWidget(QtGui.QWidget):
    """
    FaderWidget(QtGui.QWidget)

    Fades between two widgets. 
    Animation begins immediately after instantiation, 
    and the FaderWidget deletes itself upon completion.

    QWidget old_widget  - the starting widget 
    QWidget new_widget  - the ending widget 
    int     duration    - fade time in milliseconds
    bool    reverse     - do fade backwards
    """
    def __init__(self, old_widget, new_widget=None, duration=1000, reverse=False):
    
        QtGui.QWidget.__init__(self, new_widget)
        
        self.resize(old_widget.size())
        
        self.old_pixmap = QtGui.QPixmap(old_widget.size())
        old_widget.render(self.old_pixmap)
        
        self.pixmap_opacity = 1.0
        
        self.timeline = QtCore.QTimeLine()
        if reverse:
            self.timeline.setDirection(self.timeline.Backward)
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.deleteLater)
        self.timeline.setDuration(duration)

        self.timeline.start()
        self.show()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()
    
    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()



class FadeExample(QtGui.QWidget):
    """
    FadeExample(QtGui.QWidget)

    Example widget using a FaderWidget to transition 
    between two simple colored QWidgets in a stack layout. 
    """
    def __init__(self):
        super(FadeExample, self).__init__()

        self.resize(600,600)
        self.vlayout = QtGui.QVBoxLayout(self)

        self.w1 = QtGui.QWidget()
        self.w1.setStyleSheet("QWidget {background-color: red;}")

        self.w2 = QtGui.QWidget()
        self.w2.setStyleSheet("QWidget {background-color: blue;}")

        self.stacked = QtGui.QStackedLayout()
        self.stacked.addWidget(self.w1)
        self.stacked.addWidget(self.w2)

        self.vlayout.addLayout(self.stacked)
        
        self.fadeButton = QtGui.QPushButton("Fade")   
        self.resetButton = QtGui.QPushButton("Reset")

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.fadeButton)
        buttonLayout.addWidget(self.resetButton)
                
        self.vlayout.addLayout(buttonLayout)
        
        self.fadeButton.clicked.connect(self.fade)
        self.resetButton.clicked.connect(self.reset)

    def fade(self):
        FaderWidget(self.w1, self.w2)
        self.stacked.setCurrentWidget(self.w2)

    def reset(self):
        self.stacked.setCurrentWidget(self.w1)



