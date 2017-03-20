import maya.cmds as cmds

from mayaGeom import MayaGeom

#
# MayaSphere
#
class MayaSphere(MayaGeom):
    
    def __init__(self, name='Sphere'):

        MayaGeom.__init__(self)

        parts = cmds.sphere(name=name, object=True, radius=1.0)
        self.name = parts[0]
        

