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


gauge.py

Chapter07 - Gauge Progress Widget

An example of how to paint a custom widget. 
A gauge widget that can be used to indicate progress. 
"""

from PyQt4 import QtCore, QtGui

class GaugeWidget(QtGui.QWidget):
    """
    GaugeWidget(QtGui.QWidget)

    Custom Gauge Progress Widget. 
    Can accept a value between 0-1 to  
    indicate current progress.
    """

    def __init__(self, initialValue=0, *args, **kwargs):
        """
        __init__(self, float initialValue=0)

        Initialize widget with a progress value between 0-1.
        """
        super(GaugeWidget, self).__init__(*args, **kwargs)
        self.setValue(initialValue)


    def setValue(self, val):
        """
        setValue(float val)

        Set the current progress value of the gauge. 
        Values are clamped between 0-1
        """
        # clamp value between 0-1
        self._value = float(min(max(val, 0), 1))

        # schedule the gauge to repaint
        self.update()


    def value(self):
        """
        value() -> float

        Return the current progress value of the gauge
        """
        return self._value


    def paintEvent(self, event):
        """
        paintEvent(QPaintEvent event)

        Custom paint event to draw the gauge. 
        """
        # In this paint event, we start with the original 
        # rectangle region from the QPaintEvent, and progressively
        # shrink it down from the center to add more and more layers.

        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.Antialiasing)

        rect = event.rect()
        center = QtCore.QPointF(rect.center())

        painter.setPen(QtCore.Qt.NoPen)

        #
        # outer rim
        #
        grad = QtGui.QConicalGradient(center, 315)
        dark = QtGui.QColor(35,35,35)
        light = QtGui.QColor(185,185,185)
        grad.setStops([
            (0.0, dark),
            (0.5, light),
            (1.0, dark)
        ])
        painter.setBrush(grad)
        painter.drawEllipse(rect)

        #
        # inner rim
        #
        inner_bevel = self.centerScaleRect(rect, .93)
        grad.setAngle(135)
        dark = QtGui.QColor(80,80,80)
        grad.setColorAt(0.0, dark)
        grad.setColorAt(1.0, dark)
        painter.setBrush(grad)
        painter.drawEllipse(inner_bevel)

        #
        # flat gray surface
        #
        inside_panel = self.centerScaleRect(inner_bevel, .95)
        flat_gray = QtGui.QColor(50,50,50)
        painter.setBrush(flat_gray)
        painter.drawEllipse(inside_panel)

        #
        # colored gauge values
        #
        grad.setAngle(270)
        grad.setStops([
            (.2, QtGui.QColor(205,0,0)),
            (.5, QtCore.Qt.yellow),
            (.8, QtGui.QColor(0,205,0))
        ])
        painter.setBrush(grad)

        # This remaps the float value to the stop angle 
        # appropriate for the drawPie() in the paint method
        # Negative values mean clockwise
        # http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qpainter.html#drawPie
        stopAngle = self._value * -270

        # start and stop angle for drawPie() are in 1/16th of a degree
        # incriments, so we mult them by 16
        painter.drawPie(inside_panel, 225.0 * 16, stopAngle * 16)

        #
        # fill back in the inner flat gray surface (cutout)
        #
        inside_panel = self.centerScaleRect(inside_panel, .9)
        painter.setBrush(flat_gray)
        painter.drawEllipse(inside_panel)

        super(GaugeWidget, self).paintEvent(event)


    @staticmethod 
    def centerScaleRect(rect, scale):
        """
        centerScaleRect(QRect rect, float scale) -> QRect scaled

        Takes a QRect and a float scale value, and returns a copy 
        of the rect that has been scaled around the center point. 
        """
        scaledRect = QtCore.QRect(rect)

        size    = scaledRect.size()
        pos     = scaledRect.center()
        
        offset  = QtCore.QPoint(
                        pos.x() - (size.width()*.5), 
                        pos.y() - (size.height()*.5))

        scaledRect.moveCenter(offset)
        scaledRect.setSize(size * scale)
        scaledRect.moveCenter(pos)

        return scaledRect



if __name__ == "__main__":
    app = QtGui.QApplication([])
    g = GaugeWidget(.3)
    g.resize(600,600)
    g.show()
    g.raise_()
    app.exec_()

    