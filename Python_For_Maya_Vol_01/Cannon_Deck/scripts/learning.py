import maya.cmds as cmds


def gainLights(lightsList, gain):
	"""
	gainLights(list lightsList, float gain)
	
	Multiplies the value of gain, into the 
	intensity of every light in the scene.
	"""

	for light in lightsList:
		cmds.select(light, r=True)
		
		intens = cmds.getAttr(".intensity")
		newItensity = intens * gain
		
		cmds.setAttr(".intensity", newItensity)
		
		print "Light: %s, Old: %s, New: %s" % (light, intens, newItensity)
  

def createSpiral(amp=1.0, spin=30, count=20, width=3):
	"""
	createSpiral(float amp, float spin, int count, float width)
	
	Generates a spiral of spheres.
	"""
	
	height = 0
	degrees = 0
	
	count = int(count)
	
	for i in range(count):
		thisName = "SpiralSphere_%s" % i
		parts = cmds.sphere(name=thisName, pivot=[width, height, 0])
		transform = parts[0]
		
		myAttr = "%s.rotateY" % transform
		cmds.setAttr(myAttr, degrees)  
		
		height += amp
		degrees += spin
		
		if degrees >= 360:
			degrees = degrees - 360
