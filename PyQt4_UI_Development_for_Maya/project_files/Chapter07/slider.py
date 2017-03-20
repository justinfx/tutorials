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

A QSlider with a custom look using a stylesheet.

Qt Stylesheet Reference:
http://doc.qt.digia.com/4.7-snapshot/stylesheet-reference.html

"""

from PyQt4 import QtCore, QtGui
from ui import resources_rc

class Slider(QtGui.QSlider):
    """
    Slider(QtGui.QSlider)

    A QSlider with a custom stylesheet
    """
    def __init__(self, *args, **kwargs):
        super(Slider, self).__init__(*args, **kwargs)

        self.setStyleSheet("""
            QSlider::groove:horizontal {
                 border: 1px inset qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #565656, stop:1 #848484);
                 border-radius: 6px;
                 height: 10px;
                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #848484, stop:1 #919191);
                 margin: 2px 6px;
             }

             QSlider::handle:horizontal {
                 background-color: rgba(0,0,0,0);
                 image: url(:/images/slider_knob.png);
                 border: 0px;
                 width: 18px;
                 margin: -6px; 
                 border-radius: 0px;
             }
        """)

        # set the min height to there is enough drawing space
        # for the custom knob image not to get clipped
        self.setMinimumHeight(18)


class SliderExample(QtGui.QWidget):
    """
    SliderExample(QtGui.QWidget)

    Compares a standard QSlider to a custom Slider
    """
    def __init__(self):
        super(SliderExample, self).__init__()
        self.resize(300,100)

        layout = QtGui.QVBoxLayout(self)

        slider1 = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider2 = Slider(QtCore.Qt.Horizontal)

        layout.addWidget(slider1)
        layout.addWidget(slider2)

