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


channelBox.py 

Chapter06 - ChannelBox Widget

Replicating a basic working version of the Channel Box 
"""


from PyQt4 import QtCore, QtGui
import sip

from functools import partial
from contextlib import contextmanager

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as mui

from Chapter05.mqtutil import getMainWindow


class ChannelBox(QtGui.QDialog):
	"""
	ChannelBox(QtGui.QDialog)

	Custom dialog widget that emulates a few basic features 
	of the Maya Channel Box 

	1) Follows the scene selection changes 
	2) Validates attributes value types 
 	3) Can set multiple attributes values at once
	"""

	def __init__(self, *args, **kwargs):
		super(ChannelBox, self).__init__(*args, **kwargs)

		self.resize(300,500)
		self.setObjectName("CustomChannelBox")

		self._currentNode = None
		self._is_updating = False

		self.mainLayout = QtGui.QStackedLayout(self)
		self.mainLayout.addWidget(QtGui.QWidget())
		
		table = QtGui.QTableWidget(1,2)
		table.setShowGrid(False)
		table.setSpan(0,0,1,2)
		header = table.horizontalHeader()
		header.setResizeMode(0, QtGui.QHeaderView.Stretch)
		header.setVisible(False)
		table.verticalHeader().setVisible(False)
		editTriggers = table.DoubleClicked|table.SelectedClicked|table.AnyKeyPressed
		table.setEditTriggers(editTriggers)

		# Using a custom QTableWidgetItem for the second column
		# containing attribute values.
		table.setItemPrototype(AttrItem())

		node = QtGui.QTableWidgetItem()
		table.setItem(0,0,node)

		self.table = table

		self.mainLayout.addWidget(self.table)
		self.mainLayout.setCurrentIndex(1)

		self.setStyleSheet("""
		QTableWidget {
			background: rgb(65,65,65);
		}
		""")

		#
		# Connections and Callbacks
		#

		# Notify us when an item in the table is changed.
		self.table.itemChanged.connect(self.itemChanged)

		# Notify us when the scene selection changes
		self._sel_cbk_id = om.MEventMessage.addEventCallback(
							'SelectionChanged',
							self.refreshDisplay)

		# Safely delete the previous callback if this widget gets
		# deleted. Otherwise you will see a bunch of errors when it 
		# tries to fire the callback and the widget is gone.
		cbk = partial(om.MMessage.removeCallback, self._sel_cbk_id)
		self.destroyed.connect(cbk)

		# Monitor the events being sent to the table, through and
		# eventFilter method defined on this class.
		# Very useful when you don't want to have to subclass the
		# table, just to re-implement event methods.
		self.table.installEventFilter(self)



	def showEvent(self, event):
		# refreshes the attribute table to the current
		# selection, when the widget is shown
		super(ChannelBox, self).showEvent(event)
		self.refreshDisplay()


	def eventFilter(self, obj, event):
		# watch for keypresses on the table and
		# handle them directly. Make sure Maya doesn't
		# also get them and run operations on other areas
		# of the interface.
		# Accepting the event prevents it from bubbling up
		# to parent widgets.
		if obj is self.table:
			if event.type() == event.KeyPress:
				self.table.keyPressEvent(event)
				event.accept()
				# Don't pass this event on to the actual widget
				# It is filtered.
				return True

		# returning False for anything else means to just let
		# the original widget handle this event
		return False


	def itemChanged(self, item):
		"""
		itemChanged(QTableWidgetItem item)

		Slot called when an item in the attributes table is changed.
		Performs validation of the value by checking the recorded types. 
		Recursively triggers setting the same value on all other selected 
		items if a multiple selection was made.
		"""
		row = item.row()
		col = item.column()

		# we are updating the node name
		if row == 0:
			newname = cmds.rename(self._currentNode, str(item.text()))
			self.showAttributes(newname)
			return

		# we are updating an attribute value field
		elif col == 1:
			txt = str(item.text())
			attrType = type(item.attrVal)
			
			# try to convert the entered value to the type we had 
			# recorded for this attribute. If it fails to convert, 
			# then it is an invalid type. 			
			try:
				if attrType is bool:
					attrVal = txt.lower() in ('1', 'on', 'yes', 'y', 'true')
				else:
					attrVal = attrType(txt)
			
			except ValueError:
				cmds.warning("'%s' is not a valid attribute type. Expected %s" % (txt, attrType))
				with noSignals(self.table):
					item.setAttrValue(item.attrVal)
				return

			# set the attribute value on the actual node 
			cmds.setAttr(item.attrName, attrVal)
			
			# let our item reformat the text value
			with noSignals(self.table):
				item.setAttrValue(attrVal)

			# Also update every other selected item with the same
			# value. This will trigger itemChanged signals so we
			# set a flag for the first item. Subsequent calls won't
			# run this block again.
			if not self._is_updating:
				self._is_updating = True 

				for i in self.table.selectedItems():
					if i.column() != 1:
						continue
					if i is item:
						continue

					i.setAttrValue(attrVal)

				self._is_updating = False


	def refreshDisplay(self, *args, **kwargs):
		"""
		refreshDisplay()

		Slot that refreshes the ChannelBox attributes with 
		the currently selected item in the scene.
		"""
		node = ''
		sel = cmds.ls(sl=True, l=True)
		if sel:
			node = sel[-1]

		self.showAttributes(node)


	def showAttributes(self, node):
		"""
		showAttributes(str node) 

		Set the ChannelBox to view the given node. 
		If node is empty or None, the ChannelBox will simply 
		be cleared. 
		"""
		with noSignals(self.table):

			while self.table.rowCount() > 1:
				self.table.removeRow(1)

			if not node or not cmds.objExists(node):
				self._setTableVisible(False)
				return

			self._setTableVisible(True)

			# update the node name
			self._currentNode = node
			name = node.split('|')[-1]
			self.table.item(0,0).setText(name)

			# update the attributes
			attrs = cmds.listAttr(node, r=True, w=True, v=True, k=True)
			self.table.setRowCount(len(attrs)+1)

			for row, name in enumerate(attrs):

				row += 1
				self.table.setRowHeight(row, 20)

				attr = '%s.%s' % (node, name)
				niceName = cmds.attributeName(attr)

				item = QtGui.QTableWidgetItem(niceName)
				item.attrName = attr
				item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
				item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
				self.table.setItem(row, 0, item)

				val = cmds.getAttr(attr)
				item = AttrItem()
				item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
				item.setBackgroundColor(QtGui.QColor(40,40,40))
				item.attrName = attr
				item.attrVal = val 
				item.setAttrValue(val)

				self.table.setItem(row, 1, item)



	def _setTableVisible(self, v):
		# we are using a stacked widget to control 
		# visibility of the attribute table easily.
		self.mainLayout.setCurrentIndex(1 if v else 0)


	@classmethod
	def showChannelBox(cls):
		"""
		showChannelBox() -> (str dockLayout, ChannelBox widget)

		Creates a ChannelBox widget inside of a Maya dockControl. 
		Returns the dockControl path, and the ChannelBox widget.
		"""
		win = cls(parent=getMainWindow())
		size = win.size()

		name = mui.MQtUtil.fullName(long(sip.unwrapinstance(win)))

		dock = cmds.dockControl(
			allowedArea='all', 
			area='right', 
			floating=True, 
			content=name, 
			width=size.width(),
			height=size.height(),
			label='Custom ChannelBox')

		return dock, win	


@contextmanager
def noSignals(obj):
	"""Context for blocking signals on a QObject"""
	obj.blockSignals(True)
	yield
	obj.blockSignals(False)

	

class AttrItem(QtGui.QTableWidgetItem):
	"""
	AttrItem(QtGui.QTableWidgetItem)

	Custom table widget item subclass for storing 
	Maya attribute names and values

	Because we can set attributes to whatever type we want, 
	we can avoid dealing with QVariant objects through the 
	more common Qt approach of calling setData() / data()
	"""

	def __init__(self, val=None):
		super(AttrItem, self).__init__(self.UserType)

		self.attrName = ""
		self.attrVal = None

		if val is not None:
			self.setAttrValue(val)

	def setAttrValue(self, val):
		"""
		setAttrValue(object val)

		Set the value for this item. 
		Checks the type of the value against the initial 
		value type for this item when it was created. 
		"""
		if self.attrVal is not None:
			typ = type(self.attrVal)
			try:
				val = typ(val)
			except ValueError:
				val = self.attrVal
			else:
				self.attrVal = val 

			if isinstance(val, float):
				self.setText('%0.3f' % val)
			else:
				self.setText(str(val))	

