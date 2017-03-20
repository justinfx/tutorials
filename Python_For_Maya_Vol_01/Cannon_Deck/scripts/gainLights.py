def gainLights(lightsList, gain):

    for light in lightsList:
        cmds.select(light, r=True)
        
        intens = cmds.getAttr(".intensity")
        newItensity = intens * gain
        
        cmds.setAttr(".intensity", newItensity)
        
        print "Light: %s, Old: %s, New: %s" % (light, intens, newItensity)
  