"""
Sphere2

In this step we expand the Sphere class
to also have a class attribite:
    COLORS   -  tuple of colors that are allowed to be used

And we define some methods:
    setColor(color)   -  sets the color of the sphere to string name color
    setName(name)     -  sets the string name of the sphere
"""

#
# Sphere2
#
class Sphere(object):
    
    COLORS = ('red', 'green', 'blue')
    
    def __init__(self, name='Sphere', color='red'):
        self.color = color
        self.name = name
    
    def setColor(self, color):
        if color in self.COLORS:
            self.color = color
    
    def setName(self, name):
        if name:
            self.name = str(name)
            


