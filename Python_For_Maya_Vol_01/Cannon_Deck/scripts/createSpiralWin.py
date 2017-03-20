import maya.cmds as cmds
import learning


def createSpiralWin():
    window = cmds.window( title="Create Spiral", widthHeight=(200, 300) )
    cmds.columnLayout( columnAttach=('both', 5), rowSpacing=5, adjustableColumn=True )
    
    amp = cmds.floatFieldGrp( numberOfFields=1, label='Amp', value1=1.0)
    spin = cmds.floatFieldGrp( numberOfFields=1, label='Spin', value1=30)
    count = cmds.intFieldGrp( numberOfFields=1, label='Count', value1=20)
    width = cmds.floatFieldGrp( numberOfFields=1, label='Width', value1=3)

    def click(value):
        doCreateSpiral(amp, spin, count, width)
        
    cmds.button( label='Create Spiral!', command=click )
    
    closeCmd = 'cmds.deleteUI("%s", window=True)' % window
    cmds.button( label='Close', command=closeCmd )
    
    cmds.showWindow( window )


def doCreateSpiral(amp, spin, count, width):

    ampVal = cmds.floatFieldGrp(amp, query=True, value1=True)
    spinVal = cmds.floatFieldGrp(spin, query=True, value1=True)
    countVal = cmds.intFieldGrp(count, query=True, value1=True)
    widthVal = cmds.floatFieldGrp(width, query=True, value1=True)
    
    learning.createSpiral(ampVal, spinVal, countVal, widthVal)


