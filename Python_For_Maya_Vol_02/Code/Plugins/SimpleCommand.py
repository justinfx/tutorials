
"""
SimpleCommand.py plugin

A template for creating a simple command
This is usually the boiler-plate code you would copy and paste.
"""


import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys

# name our command
kPluginCmdName="SimpleCommand"

class SimpleCommand(OpenMayaMPx.MPxCommand):

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
    

    # doIt() should parse the args if needed,
    # and either do the main work of the command
    # or would call redoIt() if you are writing
    # a command that supports undo.
    def doIt(self, args):

        # parse args and set up
        sys.stdout.write("SimpleCommand.doIt(): Setting up!\n")

        # run the actual command

        # self.redoIt()
        sys.stdout.write("SimpleCommand.doIt(): Hello World\n")
    

    # If you wanted a command that supported undo,
    # then you would uncomment these and implement them
    # redoIt() should look at the args that were set up
    # in the doIt() command, and do all of the real work
    # undoIt() should be able to reverse the effects
    # of the redoIt() command.

    # def redoIt(self):
    #     sys.stdout.write("SimpleCommand.redoIt(): Hello World\n")


    # def undoIt(self):
    #     sys.stdout.write("SimpleCommand.undoIt(): Undoing!\n")
    

    def isUndoable(self):
        """
        isUndoable() -> bool
            If you are implementing the undoIt / redoIt methods
            then you would return True here so that Maya knows
            how to call your methods properly.
        """
        return False


# Creator
def cmdCreator():
    # Create the command
    return OpenMayaMPx.asMPxPtr( SimpleCommand() )

# Syntax creator
def syntaxCreator():
    """
    syntaxCreator()
        This function would define all of the flags that
        our command would accept, and set them in the MSyntax
        object.
    """
    syntax = OpenMaya.MSyntax()
    return syntax


# Initialize the script plug-in
def initializePlugin(mobject):

    # Author, Tool version, API version
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "MyName", "1.0", "Any")
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator, syntaxCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )
        raise
