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


mayaGauge2.py

Chapter07 - Maya Gauge Widget

Uses the generic gauge widget example to track 
the number of selected objects in the scene. 

Second version adds a QPropertyAnimation to the 
gauge value changes, and uses pyqtProperty decorators.
"""


from PyQt4 import QtCore, QtGui

from functools import partial

import maya.cmds as cmds
import maya.OpenMaya as om

from gauge import GaugeWidget 


class SelectionGauge(QtGui.QDialog):
    """
    SelectionGauge(QtGui.QDialog)

    Uses a Gauge widget to track the current scene selections. 

    int maxValue -  gauge is FULL when this number of characters 
                    are selected (default 5)
    """
    def __init__(self, maxValue=5, parent=None):
        super(SelectionGauge, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(400,400)

        # Don't allow anything less than 1 for the maxValue
        self.maxValue = max(maxValue, 1)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(20)

        self.text = QtGui.QLabel()
        self.text.setObjectName("statusText")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.text)

        self.gauge = GaugeWidget()

        sizePolicy = QtGui.QSizePolicy()
        sizePolicy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
        sizePolicy.setVerticalPolicy(QtGui.QSizePolicy.Expanding)

        self.gauge.setSizePolicy(sizePolicy)
        self.layout.addWidget(self.gauge)

        # Qt Stylesheet Reference:
        #   http://qt-project.org/doc/qt-4.7/stylesheet-reference.html
        # Selector Syntax: 
        #   http://doc.qt.digia.com/4.7-snapshot/stylesheet-syntax.html
        self.setStyleSheet("""
            #statusText {
                font-size   : 18px;
                color       : rgb(200,200,220);
            }
        """)

        # Notify us when the scene selection changes
        self._sel_cbk_id = om.MEventMessage.addEventCallback(
                            'SelectionChanged',
                            self.updateGauge)

        # Safely delete the previous callback if this widget gets
        # deleted. Otherwise you will see a bunch of errors when it 
        # tries to fire the callback and the widget is gone.
        cbk = partial(om.MMessage.removeCallback, self._sel_cbk_id)
        self.destroyed.connect(cbk)

        # set up an animation object
        self._value_animator = QtCore.QPropertyAnimation(self, "value")
        self._value_animator.setDuration(500)
        self._value_animator.setStartValue(0.0)
        self._value_animator.setEndValue(1.0)

        # initialize the gauge to the current scene selection, if any
        self.updateGauge()


    @QtCore.pyqtProperty(float) 
    def value(self):
        return self.gauge.value()

    @value.setter
    def value(self, val):
        self.gauge.setValue(val) 


    def updateGauge(self, *args, **kwargs):
        """
        updateGauge()

        Checks the current scene selection, and update 
        both the text label, and the gauge progress. 
        """
        sel = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(sel)
        num_selected = sel.length()

        self.text.setText("Selected %d out of %d objects" % (num_selected, self.maxValue))

        progress = float(num_selected) / self.maxValue
        currentVal = self.gauge.value()

        # animate from our current value, to our new value
        anim = self._value_animator
        anim.setStartValue(currentVal)
        anim.setEndValue(progress)
        anim.start()

