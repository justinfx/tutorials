import maya.cmds as cmds

#
# MayaGeom
#
class MayaGeom(object):
    
    def __init__(self, name='Geometry'):   
        self.name = name
        
    def setName(self, name):
        if name:
            self.name = cmds.rename(self.name, name)
            
    
    def getTranslation(self):
        return cmds.xform(self.name, query=True, translation=True)


    def setTranslation(self, x=None, y=None, z=None):
        if x is not None:
            cmds.move(x, self.name, x=True, objectSpace=True, absolute=True)
        if y is not None:
            cmds.move(y, self.name, y=True, objectSpace=True, absolute=True)
        if z is not None:
            cmds.move(z, self.name, z=True, objectSpace=True, absolute=True)



