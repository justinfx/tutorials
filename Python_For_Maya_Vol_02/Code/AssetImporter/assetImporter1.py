
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



AassetImporter1.py

This is a simple layout for the start of our
AssetImporter tool.

It defines two classes: AssetImporter and Asset

"""

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
    
    #DEFAULT_IMAGE       = "/path/to/images/defaultAsset.png"
    DEFAULT_IMAGE       = _PROJ_IMAGE

    
    DEFAULT_SHOW        = "General"

    # the attribute names that will be created on imported geometry
    ATTR_ASSET_NAME     = "assetName"
    ATTR_ASSET_SHOW     = "assetShow"

    
    def __init__(self):
        
        # public attributes are ok for users to access
        self.show = self._DEFAULT_SHOW
        
        # protected attributes should not be accessed by users.
        # Only for use internally.
        self._rootDir = ""
        
   
    def add(self, asset):
        """
        add(Asset asset) 
        
            Adds an Asset object to the Asset location
        
        """
        
        # Add asset into asset location
        
        
    def list(self, show=''):
        """
        list(string show=None)  ->  list(Asset,...)
        
            Returns a list of Asset objects currently found
            under a given show name.
            If no show is specified, return all assets.
        
        """
        
        # get list here 
        
        # return list       
        
        
        
    def load(self, name, show=''):
        """
        load(string name, string show=None) 
        
            Imports an Asset by a given name into Maya
            If no show is specified, uses the default
            show currently set in the AssetImporter
        
        """
        
        # look up Asset
        
        # load into Maya



class Asset(dict):
    """
    Asset (dict)
    
        Container object representing an Asset somewhere on
        the filesystem. Used before for defining a new Asset
        for import, and for an Asset currently in the system.
    """
    
    # name
    
    # scene file
    
    # image file
    
    # show
    
    pass    
    


          
              