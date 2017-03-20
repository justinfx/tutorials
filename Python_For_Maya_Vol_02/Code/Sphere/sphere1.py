"""
Sphere1

This step defines a new class called Sphere.
Sphere instances have two attributes:
    color   -  a string name of a color 
    name    -  a string name for the object
"""

#
# Sphere1
#
class Sphere(object):
    
    def __init__(self, name='Sphere', color=''):
        self.color = color
        self.name = name
    

