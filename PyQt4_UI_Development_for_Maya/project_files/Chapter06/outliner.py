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


outliner.py 

Chapter06 - Outliner Widget

Replicating a basic working version of the Outliner 
"""


from PyQt4 import QtCore, QtGui
import sip

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as mui

from Chapter05.mqtutil import getMainWindow


class Outliner(QtGui.QDialog):
	"""
	Outliner(QtGui.QDialog)

	Custom dialog widget that emulates a few basic features 
	of the Maya Outliner
	"""

	def __init__(self, *args, **kwargs):
		super(Outliner, self).__init__(*args, **kwargs)

		self.resize(200,500)
		self.setObjectName("CustomOutliner")

		self.layout = QtGui.QVBoxLayout(self)
		self.layout.setMargin(2)

		self.model = QtGui.QStandardItemModel()
		self.model.setItemPrototype(DagTreeItem())

		view = QtGui.QTreeView()
		view.setModel(self.model)
		view.header().setVisible(False)
		view.setEditTriggers(view.NoEditTriggers)
		view.setSelectionMode(view.ExtendedSelection)

		self.view = view
		self.layout.addWidget(self.view)

		QtCore.QTimer.singleShot(1, self.initDisplay)

		#
		# Connections
		#
		self.view.expanded.connect(self.nodeExpanded)
		self.view.selectionModel().selectionChanged.connect(self.selectionChanged)


	def initDisplay(self):
		"""
		Initialize the model with the root world items
		"""
		self.model.clear()

		excludes = set([
			'|groundPlane_transform',
			'|Manipulator1',
			'|UniversalManip',
			'|CubeCompass',
		])

		roots = self.scanDag(mindepth=1, maxdepth=2, exclude=excludes)
		if roots:
			self.model.appendColumn(roots)


	def nodeExpanded(self, idx):
		"""
		nodeExpanded(QModelIndex idx)

		Slot to handle an item in the list being expanded. 
		Populates the children of this items immediate children. 
		"""
		item = self.model.itemFromIndex(idx)

		if item.hasChildren():
		
			for row in xrange(item.rowCount()):
				child = item.child(row)
				child.removeRows(0, child.rowCount())
				grandChildren = self.scanDag(child)
				if grandChildren:
					child.appendRows(grandChildren)



	def selectionChanged(self):
		"""
		selectionChanged()

		Slot called when the selection of the view has changed. 
		Selects the corresponding nodes in the Maya scene that 
		match the selected view items.
		"""
		nodes = [self.model.itemFromIndex(i).fullname for i in self.view.selectedIndexes()]
		if nodes:
			cmds.select(nodes, replace=True)
		else:
			cmds.select(clear=True)



	@staticmethod
	def scanDag(root=None, mindepth=1, maxdepth=1, exclude=None):
		"""
		scanDag(root=None, mindepth=1, maxdepth=1, exclude=None) -> list 

		root 		- either an MDagPath or DagTreeItem to start from 
		mindepth 	- starting depth of items to return (default 1; immediate children)
		maxdepth 	- ending depth of items to return (default 1; immediate children)
		exclude 	- a sequence of strings representing node paths that should be skipped

		Walks the DAG tree from a starting root, through a given depth 
		range. Returns a list of the top level children of the root as 
		DagTreeItem's. Decendants of these items already have been added 
		as DagTreeItem children. 

		mindepth or maxdepth may be set to -1, in which case those limits will 
		be ignored altogether.
		"""
		# Allow either a DagTreeItem or an MDagPath
		if isinstance(root, DagTreeItem):
			root = root.dagObj

		dagIt = om.MItDag()
		root = root or dagIt.root()
		exclude = exclude or set()

		dagIt.reset(root, om.MItDag.kDepthFirst)

		# These will be our final top-most nodes from the search
		nodes = []

		# This will map node string paths to the items to help us
		# easily look up a parent at any point in the search.
		itemMap = {}

		while not dagIt.isDone():

			depth = dagIt.depth()

			# if the iterator has gone past our target
			# depth, prune out the tree from here on down,
			# so it is not used in future loops
			if (maxdepth > -1) and (depth > maxdepth):
				dagIt.prune()

			# this would allow us to skip past an amount of
			# levels from the root, if mindepth > 1
			elif depth >= mindepth:
				dagPath = om.MDagPath()
				dagIt.getPath(dagPath)
				path = dagPath.fullPathName()

				if path and path not in exclude:
					item = DagTreeItem(dagPath)

					# save this item in our mapping
					itemMap[item.fullname] = item

					# If this item has a parent, add it to that
					# parent DagTreeItem. 
					# Otherwise, just add it to our top level list
					parent = itemMap.get(item.parentname)
					if parent:
						parent.appendRow(item)
					else:
						nodes.append(item)

				# prune out items that were in our excludes list
				else:
					dagIt.prune()

			dagIt.next()

		return nodes



	@classmethod
	def showOutliner(cls):
		"""
		showOutliner() -> (str dockLayout, Outliner widget)

		Creates a Outliner widget inside of a Maya dockControl. 
		Returns the dockControl path, and the Outliner widget.
		"""
		win = cls(parent=getMainWindow())
		size = win.size()

		name = mui.MQtUtil.fullName(long(sip.unwrapinstance(win)))

		dock = cmds.dockControl(
			allowedArea='all', 
			area='left', 
			floating=False, 
			content=name, 
			width=size.width(),
			height=size.height(),
			label='Custom Outliner')

		return dock, win	


class DagTreeItem(QtGui.QStandardItem):
	"""
	DagTreeItem(QtGui.QStandardItem)

	QStandardItem subclass that represents a Dag node
	"""
	def __init__(self, dagObj=None):
		super(DagTreeItem, self).__init__()

		self.dagObj = dagObj

		self.setText(self.name)

	def __repr__(self):
		return "<%s: %s>" % (self.__class__.__name__, self.name)


	@property 
	def fullname(self):
		if not self.dagObj:
			return ''

		return self.dagObj.fullPathName()

	@property 
	def name(self):
		return self.fullname.rsplit('|', 1)[-1]


	@property 
	def parentname(self):
		return self.fullname.rsplit('|', 1)[0]

		

