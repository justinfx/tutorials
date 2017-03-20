def createSpiral(amp=1.0, spin=30, count=20, width=3):

    height = 0
    degrees = 0
    
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