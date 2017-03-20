"""
Simple benchmark test:
    maya.cmds vs PyMel vs Python API

    1. Create a polyHelix that has about 20k vertices. 
    2. Loop over each vertex and move it by a random amount
    3. Delete the helix
"""


import sys
import time
import random

# python commands test
import maya.cmds as cmds

# pymel test
import pymel.core as pm

# python api test
import maya.OpenMaya as OpenMaya



# options for cmds.polyHelix()
# 20020 vertices
HELIX_OPTS = dict( ch=True, o=True, c=20, h=30, w=4, r=.3, sa=20, sco=50 )


# The faster test. Produces even more of a speed difference.
# Less subdivisions ( ~3000 vertices )

HELIX_OPTS["sa"] = 2


# random movement range
RAND    = random.Random(0)
LOW     = -4
HIGH    = 4


def testPyCmds():

    start = time.time()

    helix = cmds.polyHelix(**HELIX_OPTS)
    pHelix = helix[0]

    size = cmds.polyEvaluate(v=True)

    for i in xrange(size):
        x = RAND.uniform(LOW, HIGH)
        attrib = '%s.vtx[%s]' % (pHelix, i)
        cmds.move(x, attrib, x=True)
    
    cmds.delete(pHelix)

    end = time.time()
    return end-start


def testPyApi():

    start   = time.time()

    # creating the helix via the cmds module, for consistency
    # in the helix object and number of vertices
    helix   = cmds.polyHelix(**HELIX_OPTS)
    pHelix  = helix[0]

    sel     = OpenMaya.MSelectionList()
    node    = OpenMaya.MObject()

    sel.add(pHelix)
    sel.getDependNode( 0, node ) 

    vector = OpenMaya.MVector()

    iter = OpenMaya.MItMeshVertex(node)

    while not iter.isDone():

        vector.x = RAND.uniform(LOW, HIGH)
        iter.translateBy(vector)

        iter.next()
    
    OpenMaya.MGlobal.deleteNode(node)

    end = time.time()
    return end-start


def testPyMel():

    start = time.time()

    helix = pm.polyHelix(**HELIX_OPTS)
    pHelix = helix[0]

    # 20020 loops
    for v in pHelix.vtx:

        # strangly, its faster to make a new vector
        # object every time, as opposed to creating it
        # once and changing the x value each time???
        vector = pm.dt.Vector(x=RAND.uniform(LOW, HIGH))
        v.translateBy(vector)
    
    pm.delete(pHelix)

    end = time.time()
    return end-start


def testAll():
    results = []

    sys.stdout.write("Testing testPyCmds()\n")
    sys.stdout.flush()

    r = testPyCmds()
    results.append((r, "PyCmds"))

    sys.stdout.write("Testing testPyMel()\n")
    sys.stdout.flush()
        
    r = testPyMel()
    results.append((r, "PyMel"))

    sys.stdout.write("Testing testPyApi()\n")
    sys.stdout.flush()

    r = testPyApi()
    results.append((r, "PyApi"))

    results.sort()
    fastest = results.pop(0)

    print "\nResults from fastest to slowest..."
    print "%s:\t%0.4f sec" % (fastest[1], fastest[0])

    for r in results:
        diff = r[0] / fastest[0]
        print "%s:\t%0.4f sec (%0.2fx slower than %s)" % (r[1], r[0], diff, fastest[1])
