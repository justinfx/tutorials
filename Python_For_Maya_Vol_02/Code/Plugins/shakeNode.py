
"""
Copyright (c) 2011, Justin Israel (justinisrael@gmail.com) 
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



shakeNode.py

A dependency graph node plugin.
Creates a shake generator using a perlin noise function.

Uses pnoise.py which should be found in the same directory
as this file. 

This should be placed in your MAYA_PLUG_IN_PATH location, or you
can load it directly for testing purposes:

PYTHON usage:
	import maya.cmds as cmds
	cmds.loadPlugin("/path/to/shakeNode.py")
    shake = cmds.createNode("shakeNode")
    cmds.connectAttr("time1.outTime", "%s.time" % shake)

"""

import math, sys, random

# pnoise.py should be in the same directory
from pnoise import pnoise

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# give our node a name
kPluginNodeTypeName = "shakeNode"

# This is required by Maya. 
# Each node must have a unique ID so that it can
# properly be identified when reading and writing the
# scene files. 
# See this link for more details about the ranges
# you can use:
# http://tinyurl.com/MTypeId
shakeNodeId = OpenMaya.MTypeId(0x90000)


# Node definition
# MPxNode is the base class for any type of new node in Maya
class ShakeNode(OpenMayaMPx.MPxNode):

	# These are just references to our attribues
	# to allow us to look up their values.
	# They dont actually hold data.

	# input attributes
	amp 	= OpenMaya.MObject()
	freq 	= OpenMaya.MObject()
	seed 	= OpenMaya.MObject()
	time 	= OpenMaya.MObject()
	octaves = OpenMaya.MObject()

	# output attributes
	output 	= OpenMaya.MObject()


	# Should make sure to call the init on the superclass
	# Though we arent doing anything special in the __init__()
	def __init__(self):
		super(ShakeNode, self).__init__()
	

	# The compute method is an override that
	# you must provide to a new node class.
	# It receives the plug that has become dirty and
	# the current data values that are available
	# to you during this evaluation.
	def compute(self, plug, dataBlock):

		# we are only computing a single output plug
		if ( plug == self.output ):

			# Get all of the input values from the datablock,
			# using our attribute references.
			amp 	= dataBlock.inputValue(self.amp).asFloat3()
			freq 	= dataBlock.inputValue(self.freq).asFloat3()
			mTime	= dataBlock.inputValue(self.time).asTime()
			octaves	= dataBlock.inputValue(self.octaves).asInt()
			seed 	= dataBlock.inputValue(self.seed).asLong()
			secs	= float(mTime.asUnits(mTime.kSeconds))

			# We use an offset seed number for the Y axis
			# to make sure that the curves are not identical
			x = self.getShake(secs, freq[0], amp[0], seed, octaves)
			y = self.getShake(secs, freq[1], amp[1], seed + 250, octaves)	
			z = self.getShake(secs, freq[2], amp[2], seed + 500, octaves)		

			outputHandle = dataBlock.outputValue(self.output)
			outputHandle.set3Float(x, y, z)

								
			# Setting the output plug to clean means that
			# the node won't have to re-evaluate until an
			# input plug gets modified. Though since one
			# of our inputs is a time value, this node will
			# re-evaluate on every frame.
			dataBlock.setClean(plug)

			return OpenMaya.MStatus.kSuccess

		return OpenMaya.kUnknownParameter


	def getShake(self, t, freq, amp, seed=0, octaves=3):
		"""
		getShake (float t, float freq, float amp, int seed = 0, int octaves = 3) -> float noise

			A wrapper around the pnoise() function that produces a fractal sum
			by using the octaves value to generate values multiple times
			with increasing frequency and decreasing amplitude.

			float t  	- the time value, or other changing value
			float freq 	- fequency of the curve values (speed)
			float amp 	- amplitude of the curve values (intensity)
			int seed 	- Any random number. The seed number lets you change the randomization
			int octaves - Creates finer detail (jitter) in the curve values
		"""

		val = 0

		if amp == 0 or freq == 0:
			return val
		
		# underscore is a special symbol to throw away the
		# value since we dont care about it.
		for _ in range(octaves):

			val += pnoise( (t + seed) * freq ) * amp
			
			# modify the freq and amp for the next octave
			freq *= 2
			amp /= 2 
		
		return val


# Every node plugin needs a nodeCreate() method
# Maya expects to use this to know how to get a
# new instance of your node class.
def nodeCreator():
	return OpenMayaMPx.asMPxPtr( ShakeNode() )


# Maya expects this function, to initialize
# the node class ONCE when the plugin is loaded
# It sets up the attributes
def nodeInitializer():

	nAttr = OpenMaya.MFnNumericAttribute()
	uAttr = OpenMaya.MFnUnitAttribute()

	# input

	ShakeNode.amp = nAttr.create( "amplitude", "amp", OpenMaya.MFnNumericData.k3Float, 1.0 )
	nAttr.setStorable(True)
	nAttr.setKeyable(True)

	ShakeNode.freq = nAttr.create( "frequency", "freq", OpenMaya.MFnNumericData.k3Float, 1.0 )
	nAttr.setStorable(True)
	nAttr.setKeyable(True)

	ShakeNode.seed = nAttr.create( "randomSeed", "seed", OpenMaya.MFnNumericData.kLong, 1000 )
	nAttr.setStorable(True)
	nAttr.setKeyable(False)
	nAttr.setMin(0)

	ShakeNode.octaves = nAttr.create( "octaves", "oct", OpenMaya.MFnNumericData.kInt, 3 )
	nAttr.setStorable(True)
	nAttr.setKeyable(True)
	nAttr.setMin(2)
	
	# the time attribute should be connected to the default "time1" node
	# or any time node to provide a changing time value
	ShakeNode.time = uAttr.create( "currentTime", "time" , OpenMaya.MFnUnitAttribute.kTime,  0.0 )
	uAttr.setHidden(True)
	nAttr.setStorable(False)
		
	# output
	ShakeNode.output = nAttr.create( "output", "out", OpenMaya.MFnNumericData.k3Float, 0.0 )
	nAttr.setStorable(False)
	nAttr.setWritable(False)
	nAttr.setHidden(False)


	# add attributes to the node
	ShakeNode.addAttribute( ShakeNode.amp )
	ShakeNode.addAttribute( ShakeNode.freq )
	ShakeNode.addAttribute( ShakeNode.seed )
	ShakeNode.addAttribute( ShakeNode.time )
	ShakeNode.addAttribute( ShakeNode.octaves )
	ShakeNode.addAttribute( ShakeNode.output )

	# when one attribute is changed, it will cause
	# the other to become "dirty", meaning that its value
	# should be computed again
	ShakeNode.attributeAffects( ShakeNode.amp, ShakeNode.output )
	ShakeNode.attributeAffects( ShakeNode.freq, ShakeNode.output )
	ShakeNode.attributeAffects( ShakeNode.seed, ShakeNode.output )
	ShakeNode.attributeAffects( ShakeNode.octaves, ShakeNode.output )
	ShakeNode.attributeAffects( ShakeNode.time, ShakeNode.output )
	


# initialize the script plug-in
def initializePlugin(mobject):

	# sets the Author, Version, and API version
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Justin Israel", "1.0", "ANY")
	try:
		mplugin.registerNode( kPluginNodeTypeName, shakeNodeId, nodeCreator, nodeInitializer )
	except:
		sys.stderr.write( "Failed to register node: %s" % kPluginNodeTypeName )
		raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( shakeNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeTypeName )
		raise
	
