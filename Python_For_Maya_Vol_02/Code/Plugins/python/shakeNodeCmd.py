"""
shakeNodeCmd.py

Helper command for creating and returning a new
shakeNode from our plugin.

"""

import maya.cmds as cmds

def createShakeNode(transform=None):
	"""
	createShakeNode (string transform=None) -> string node

		A helper command for creating a new shakeNode
		Optionally, a transform node path may be given
		to automatically connect the shakeNode output
		into the transform input.
	"""
	
	if not cmds.pluginInfo("shakeNode", query=True, loaded=True):
		cmds.error("shakeNode plugin is not loaded!")
	
	shake = cmds.createNode("shakeNode")
	cmds.connectAttr("time1.outTime", "%s.time" % shake)

	if transform:

		if not cmds.objExists(transform):
			cmds.error("transform does not exist: %s" % transform)

		cmds.connectAttr("%s.output" % shake, "%s.translate" % transform, f=True)

	return shake

