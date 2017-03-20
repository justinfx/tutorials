import maya.cmds as cmds

from mayaGeom import MayaGeom

#
# MayaSphere
#
class MayaSphere(MayaGeom):
    
    def __init__(self, name='Sphere', **kwargs):

        MayaGeom.__init__(self)
            
        kwargs['name'] = name
        kwargs['object'] = True
     
        parts = cmds.sphere(**kwargs)
        self.name = parts[0]
        
           
    def setTranslation(self, x=None, y=None, z=None):
        
        for name in ('x','y','z'):
            val = locals()[name]
            if val is not None:
                opts = {name:True, 'objectSpace':True, 'absolute':True}
                cmds.move(val, self.name, **opts)

    def getRotation(self):
        return cmds.xform(self.name, query=True, rotation=True)


    def setRotation(self, x=None, y=None, z=None):
        
        for name in ('x','y','z'):
            val = locals()[name]
            if val is not None:
                opts = {name:True, 'objectSpace':True, 'absolute':True}
                cmds.rotate(val, self.name, **opts)

    def getScale(self):
        return cmds.xform(self.name, query=True, scale=True)

    def setScale(self, x=None, y=None, z=None):
        
        for name in ('x','y','z'):
            val = locals()[name]
            if val is not None:
                opts = {name:True, 'objectSpace':True, 'absolute':True}
                cmds.scale(val, self.name, **opts)




