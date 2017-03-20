
"""
Copyright (c) 2011, Justin Israel (justinisrael@gmail.com) 
All rights reserved. 

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met: 

 * Redistributions of source code must retain the above copyright notice, 
   this list of conditions and the following disclaimer. 
 * Redistributions in binary form must reproduce the above copyright 
   notice, this list of conditions and the following disclaimer in the 
   documentation and/or other materials provided with the distribution. 
 * Neither the name of cmiVFX.com nor the names of its contributors may be 
   used to endorse or promote products derived from this software without 
   specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE. 



assetImporter4.py

This version adds more functionalty:
    * listing current shows
"""

import os
import shutil
import re
import maya.cmds as cmds



# These are special defaults for use in the project examples
# You can change the locations where they are used to real paths
# if you want.
_PROJ_ROOT      = os.path.join( os.path.dirname(__file__), "../../" )
_PROJ_ASSETS    = os.path.join( _PROJ_ROOT, "AssetLibrary" ) 
_PROJ_IMAGE     = os.path.join( _PROJ_ROOT, "Images/defaultAsset.png" )



class AssetImporter(object):
    """
    AssetImport
    
    Simple Asset Manager tool allowing the user to:
        * list assets available
        * add new assets
        * import an asset into Maya
    
    Supports the separation of assets by "show" names.
    
    """
    
    # class attributes are constant values that are provided
    # to every instance of AssetImporter.
    
    #ASSETS_LOCATION     = "/path/to/AssetLibrary"
    ASSETS_LOCATION     = _PROJ_ASSETS
    
    #DEFAULT_IMAGE       = "path/to/images/defaultAsset.png"
    DEFAULT_IMAGE       = _PROJ_IMAGE

    
    DEFAULT_SHOW        = "General"

    # the attribute names that will be created on imported geometry
    ATTR_ASSET_NAME     = "assetName"
    ATTR_ASSET_SHOW     = "assetShow"



    def __init__(self, show='', verbose=False):
        
        # public attributes are ok for users to access
        self.verbose    = verbose
        
        # protected attributes should not be accessed by users.
        # Only for use internally.
        self._rootDir   = ""
        
        self.show = show or self.DEFAULT_SHOW

        # make sure the root location exists
        self.setAssetRoot(self.ASSETS_LOCATION)

    # This is a computed property. It works like a
    # normal attribute for getting a value, but computes
    # that value on demand. In this case, it also is READ-ONLY
    @property
    def showDir(self):
        """ Full path to current show directory  """
        return os.path.join(self._rootDir, self.show)

    @property
    def show(self):
        return self._show
    
    @show.setter
    def show(self, s):
        if not re.match(r'[a-zA-Z_.-]+', s):
            raise ImporterException('show "%s" is not a valid show format. Must contain only [a-zA-Z_.-]' % s)
        
        self._show = s
    

    def add(self, asset):
        """
        add(Asset asset) 
        
            Adds an Asset object to the Asset location.
            The Asset will be updated to reflect its new imported location.
        
        """
        
        # perform all basic checks on the Asset object
        if not isinstance(asset, Asset):
            # raise a general python Exception
            raise TypeError("Argument type %s is not an Asset instance" % type(asset))
        
        if not asset.scene or not os.path.isfile(asset.scene):
            # raise our custom Exception
            raise ImporterException("Asset must have a valid scene attribute set and must exist")
        
        show    = asset.show or self.show
        d       = self._getShowDir(asset.show)
        
        # scene file and name format
        fileName    = os.path.basename(asset.scene)
        name, ext   = os.path.splitext(fileName)
       
        name        = asset.name or name
        newName     = "%s%s" % (name, ext)
        destFile    = os.path.join(d, newName)
        
        # image file format
        img     = asset.image or self.DEFAULT_IMAGE
        ext     = os.path.splitext( os.path.basename(img) )[-1]
        imgName = "%s%s" % (name, ext)
        imgFile = os.path.join(d, 'images', imgName)
        
        # Dont allow importing of duplicate asset names
        if os.path.exists(destFile):
            # raise our own special Exception that can be caught
            # specifically, as opposed to general python errors.
            raise ImporterException("Asset already exists: %s" % destFile)
        
        
        # now add to the library
        shutil.copy(asset.scene, destFile)
        shutil.copy(img, imgFile)


        # update the Asset object
        asset.name  = name
        asset.scene = destFile
        asset.image = imgFile
        asset.show  = show

        self._print("=> Added: %s" % asset)

        
    def list(self, name='', allShows=False):
        """
        list(string name='', bool allShows=False)  ->  list(Asset,...)
        
            Returns a list of Asset objects currently found
            under the current show.
            If allShows == True, return matching assets in all shows.
            
            Specifying a name returns only Assets whose asset.name contains
            the given name. i.e.
            name = 'Asset' can return:
                MyAsset1, Asset, Asset50, OldAsset
        
        """
        
        dirs = []
        
        if allShows:
            for item in os.listdir(self._rootDir):
                full = os.path.join(self._rootDir, item)
                if os.path.isdir(full):
                    dirs.append(full)
       
        else:
            dirs.append( self._getShowDir() )

      
            
        assets = []
        
        for d in dirs:
            
            show = os.path.basename(d)
            
            for item in os.listdir(d):
                
                if item.startswith("."):
                    continue
                
                full = os.path.join(d, item)
               
                if os.path.isfile(full):
                    
                    aName = os.path.splitext(item)[0]
                    # if a specific asset name was given, and
                    # this one isnt it.. move on
                    if name and not name in item:
                        continue

                    imgExt  = os.path.splitext(self.DEFAULT_IMAGE)[1]
                    imgFile = '%s%s' % (aName, imgExt)
                    
                    asset = Asset()
                    asset['scene']  = full
                    asset['name']   = aName
                    asset['show']   = show 
                    asset['image']  = os.path.join(d, 'images', imgFile)    
                    
                    assets.append(asset)
       
        
        return assets
        

    def listShows(self):
        """
        listShows()  ->  list of show names
        
            Return a list of show names currently existing in the Asset Library
        
        """

        shows = []
        for item in os.listdir(self._rootDir):
            full = os.path.join(self._rootDir, item)
            if os.path.isdir(full):
                shows.append(item)
 
        return shows

                
    def load(self, obj):
        """
        load(string/Asset obj) 
        
            Imports an Asset by a given name or Asset into Maya
        """

        if isinstance(obj, Asset):
            assets = [obj]
        else:
            assets = self.list(name)

        self._print("Loading %d assets..." % len(assets))

        cmds.select(clear=True)

        for asset in assets:

            before = set(cmds.ls(assemblies=True, r=True))
            cmds.file(asset.scene, namespace=asset.name, r=True, gl=True, loadReferenceDepth="all")
            after = set(cmds.ls(assemblies=True, r=True))

            newStuff = after.difference(before)

            for item in newStuff:

                cmds.addAttr(item, longName=self.ATTR_ASSET_NAME, dataType="string")
                cmds.addAttr(item, longName=self.ATTR_ASSET_SHOW, dataType="string")

                cmds.setAttr("%s.%s" % (item, self.ATTR_ASSET_NAME), asset.name, type="string")
                cmds.setAttr("%s.%s" % (item, self.ATTR_ASSET_SHOW), asset.show, type="string")
            
            self._print("=> Loaded: %s" % asset)

            cmds.select(list(newStuff), add=True)


    def findImported(self):
        """
        findImported()  ->  list of (str nodeName, Asset)
            
            Searches the scene for all assets that have been imported
            and returns a list of tuples. The first element of each
            tuple is the name of the top node of the item in the scene,
            and the second element is the Asset object.
        """

        transforms = cmds.ls(type="transform", long=True)
        if not transforms:
            return []
        
        results = []

        for t in transforms:
            
            if not cmds.attributeQuery(self.ATTR_ASSET_NAME, node=t, exists=True):
                continue
            
            name = cmds.getAttr("%s.%s" % (t, self.ATTR_ASSET_NAME))
            show = cmds.getAttr("%s.%s" % (t, self.ATTR_ASSET_SHOW))

            self.show = show
            asset = self.list(name)

            if asset:
                asset = asset[0]
            else:
                asset = None

            results.append( (t, asset) )

        return results
        

    def setAssetRoot(self, root):
        """
        setAssetRoot(string root) 
        
            Set the root level directory for the Asset manager.
            Show directories will live under this root, and
            Assets will live under shows.
            Creates the directory if it does not exist.
        """
        
        if not os.path.exists(root):
            
            try: 
                os.mkdir(root)
            
            except OSError, e:
                cmds.error("Could not create asset root directory. %s" % e)
        
        self._rootDir = root
    

    # Method names starting with an underscore is considered
    # "protected", meaning outside users shouldn't need to
    # use this, as its for internal use. But subclasses of
    # this class can still access it.
    def _getShowDir(self, show=''):
        """
        _getShowDir(string show='')  ->  string path
        
            Get the full path to a show directory, and create it if it 
            doesn't exist. If no show name is given, return the 
            current set show
        """
        
        if show:
            d = os.path.join(self._rootDir, show)
        else:
            d = self.showDir
        
        if not os.path.exists(d):
           
            try:
                os.mkdir(d)
                
            except OSError, e:
                cmds.error("Failed to create show directory '%s'. %s" % (d, e))

        
        imgDir = os.path.join(d, 'images')
        
        if not os.path.exists(imgDir):
           
            try:
                os.makedirs(imgDir)
                
            except OSError, e:
                cmds.error("Failed to create show image directory '%s'. %s" % (imgDir, e))
                                
        return d
    

    def _print(self, msg):
        """
        _print (string msg)

            Helper method that only prints if verbose == True
        """
        if self.verbose:
            print msg   


class ImporterException(Exception):
    """
    ImporterException (Exception)
    
    An empty subclass of Exception, for returning
    AssetImporter-specific error that we can catch.
    """
    pass




class Asset(dict):
    """
    Asset (dict)
    
        Container object representing an Asset somewhere on
        the filesystem. Used before for defining a new Asset
        for import, and for an Asset currently in the system.
    """    
    
    def __init__(self):
        
        super(Asset, self).__init__()
        
        for val in ('name', 'show', 'scene', 'image'):
            self[val] = ''
    

    def __repr__(self):
        """
        __repr__()
        
            Specifies the formatted representation of the class,
            when printing.
        """
        
        # Since Asset subclasses a dictionary, we can use self as a string formatter
        
        return "\nName: %(name)s \n\t Show: %(show)s \n\tScene: %(scene)s \n\tImage: %(image)s" % self
    
    
    # a getter property
    @property
    def name(self):
        return self.get('name', '')
    
    # a setter property - this make Asset.name read AND write capable.
    @name.setter
    def name(self, val):
        self['name'] = val

    @property
    def show(self):
        return self.get('show', '')

    @show.setter
    def show(self, val):
        self['show'] = val

    @property
    def scene(self):
        return self.get('scene', '')

    @scene.setter
    def scene(self, val):
        self['scene'] = val
        
    @property
    def image(self):
        return self.get('image', '')

    @image.setter
    def image(self, val):
        self['image'] = val  




#
# Running in stand-alone mode.
#
# Example on Linux/OSX:
#
#    export MAYA_LOCATION=/path/to/maya/directory
#    $MAYA_LOCATION/bin/mayapy assetImporter.py
#
if __name__ == "__main__":
    
    import optparse
    import sys

    usage = "usage: %prog --show=SHOW [assetName]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-s", "--show", default='', help='Search under a specific show name')

    (options, args) = parser.parse_args()

    name        = args[0] if args else ''
    allShows    = False if options.show else True


    # we initialize maya AFTER checking args so that
    # it wont take as long to just get help with  -h 
    import maya.standalone
    maya.standalone.initialize(name="python")


    # this is how we catch our custom Exception
    # instead of the program just crashing.
    try:
        importer = AssetImporter()
        if options.show:
            importer.show = options.show

    except ImporterException, e:
        print "Error: ", e
        # any non-zero exit status means an error. 1 is a general error
        sys.exit(1)


    for a in importer.list(name, allShows):
        print a    
          
              