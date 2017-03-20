
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


Description:
A progression of MayaSphere class examples showing
the concept of a class structure, and inheritence.

MayaSphere wraps some common functions of a sphere
geometry into an object-oriented structure.

=============================

MayaSphere4 Examples:

# create 5 spheres
sphereList = []
for i in range(5):
    sphereList.append(MayaSphere4(name="MayaSphereTest")) 

# organize
cmds.select(*sphereList)  # expand to single parameters
cmds.align(x='stack')

# play with values
sphereList[2].setScale(2,2)
sphereList[0].setTranslation(y=3.25)
sphereList[4].setRotation(x=45, z=90)
print sphereList[0].getTranslation()

# delete third item in list directly
sphereList[2].delete()
print sphereList[2], "Exists?", sphereList[2].exists()

# delete first item in list indirectly
del sphereList[0]

# delete the rest automatically
del sphereList


=============================
Inheritence Example:

poly = PolySphere()
poly.setScale(x=2)  # has all functionality of superclass MayaSphere

"""

import maya.cmds as cmds

from mayaGeom import MayaGeom

#
# MayaSphere
#
class MayaSphere(MayaGeom):
    """
    MayaSphere (MayaGeom)
    
    Base class for creating a sphere with default settings (Nurbs)
    
    A subclass should redefine _create() method, to define a new
    way to create the geometry.
    """
    
    def __init__(self, name='Sphere', **kwargs):

        MayaGeom.__init__(self)
        
        kwargs['name'] = name
        kwargs['object'] = True

        self._create(kwargs)
    
    def __del__(self):
        """
        This is just an interesting example of built-in methods
        of python objects. Normally you wouldn't use __del__ like
        this to delete the maya geometry when the python object
        is deleted, but it shows a visual representation of python
        cleaning up its data.
        
        Notice what happens when you do this:
            
            s = MayaSphere(name="FirstSphere")
            s.setScale(2,2,2)
            s = MayaSphere(name="SecondSphere")
        
        The FirstSphere is deleted and replaced with SecondSphere,
        because the variable was overwritten and __del__ was called
        on the first object after reassigning.
        """
        self.delete()
    
    def __str__(self):
        return self.name
    
    def _create(self, opts={}):
        parts = cmds.sphere(**opts)
        self.name = parts[0]        
    
    def delete(self):
        if self.exists():
            cmds.delete(self.name)
    
    def exists(self):
        return cmds.objExists(self.name)

    def setTranslation(self, x=None, y=None, z=None):
        self._doTransform(cmds.move, x, y, z)

    def getRotation(self):
        return cmds.xform(self.name, query=True, rotation=True)

    def setRotation(self, x=None, y=None, z=None):
        self._doTransform(cmds.rotate, x, y, z)

    def getScale(self):
        return cmds.xform(self.name, query=True, scale=True)

    def setScale(self, x=None, y=None, z=None):
        self._doTransform(cmds.scale, x, y, z)

    def _doTransform(self, func, x, y, z):
        for name in ('x','y','z'):
            val = locals()[name]
            if val is not None:
                opts = {name:True, 'objectSpace':True, 'absolute':True}
                func(val, self.name, **opts)
    

#
# PolySphere
#
class PolySphere(MayaSphere):
    """
    PolySphere
    
    Subclass of MayaSphere, but creates a polySphere.
    All the original parent methods should work the same,
    but if they needed changes, we could overload the
    ones we want, just like we do for _create()
    """
    
    def __init__(self, name='PolySphere', **kwargs):
        # When we subclass another object and we want to modify its
        # __init__() we should make sure to also call the __init__
        # on the superclass to it does all the original set up
        MayaSphere.__init__(self, name, **kwargs)
        
        # we could do more specific setup stuff now
        # [here]
    
    def _create(self, opts={}):   
        """
        Overload _create() method from MayaSphere with a new
        one that will generate a polySphere instead.
        """
        parts = cmds.polySphere(**opts)
        self.name = parts[0]
