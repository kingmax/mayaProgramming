# Maya Wire Plugin
This plugin enables fast and easy creation of wires, cables, pipes, ribbons, ropes and other shapes that can be built on a curve inside of Autodesk Maya. All you have to do is create a NURBS curve, select it and invoke *wireMeshFromCurve* command available under Maya *Create > Wire Tools* menu (also works with multiple curves selected).

## Current status
### Version: 0.2.1
#### Features
- wireMeshCreator node.
    - New wire profiles:
        - RPolygon - regular polygon generation for wire profiles (+ star polygons),
        - Pattern - create linear or circular patterns for wire profiles, thus allowing creation of ropes, parallel cables and more, using only one curve.
    - New interpolation range: Distance.
    - Added normals management inside node:
		- Reverse normals attribute,
		- Smoothing angle attribute.
- wireMeshFromCurve command.
    - Now automatically renames newly created transform and mesh nodes to: wire# and wireShape#.
- New icons that matches Maya's color scheme for polygonal modeling (orange).

#### Fixes
- Unable to load wireMeshCreator node attributes values to Attribute Editor when this node is created for the first time in Maya session.
- *Wire Mesh from Curve* menu item does not add proper command to a shelf when it is Ctrl+Shift+LMB from menu. 
- Maya crashes on undo/redo of wireMeshFromCurve command.
- Inability to properly keyframe and animate on wireMeshCreator node.
- Inappropriate behavior when curve is intersecting with itself.
- Icon for wireMeshCreator node not showing in Node Editor.
- *wireMeshFromCurve* command giving an error because python *cmds* namespace is not visible inside Maya by default.
    
#### Notes
- Removed following wire profiles (replaced by more general RPolygon):
    - Circle8,
    - Square.
- Plugin was tested inside Maya 2017 Update 1 and Maya 2018 Update 1 on Windows 10.

## Installation
Download ZIP file from [Autodesk App Store](https://apps.autodesk.com/) (search for *Wire* in Maya section). Unpack ZIP file on your system and put *wire* folder and *wire.mod* file in [*MAYA_MODULE_PATH* directory](http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=GUID-228CCA33-4AFE-4380-8C3D-18D23F7EAC72#GUID-228CCA33-4AFE-4380-8C3D-18D23F7EAC72__WS1A9193826455F5FF-4855151011E4FD543C6-3527). If folder called *modules* does not exists, create it. 

Possible paths:
- (Windows): `%USERPROFILE%/Documents/maya/<maya_version>/modules/`
- (MacOS): `$HOME/Library/Preferences/Autodesk/maya/<maya_version>/modules/`
- (Linux): `$HOME/maya/<maya_version>/modules/`

Open Maya and then open Plug-in Manager window. Search for *wire.py* plugin, it should be in its own tab. Now just simply check *Loaded* checkbox and you are ready to go (also *Auto load* if you want this plugin to be loaded automatically next time you open Maya).

## How to use
Every wire needs a path. Create a NURBS curve with either tool available in Maya *Create > Curve Tools* menu. With the curve selected go to *__Create > Wire Tools__* menu and click at *__Wire Mesh from Curve__*, this will invoke *wireMeshFromCurve* command which will create two things for you: polygon mesh and *__wireMeshCreator__* node. Latter is the core node of the plugin and it is responsible for generating polygon mesh data. At this point Attribute Editor should be visible and show *wireMeshCreator* attributes that you can modify.

Note that you can have multiple curves selected while calling *wireMeshFromCurve* command. By default this will create single *wireMeshCreator* node that will operate on multiple curves generating the same amount of mesh nodes. To create one *wireMeshCreator* per curve invoke this command with *oneNodePerCurve* flag set to `True`.

```
import maya.cmds as cmds
cmds.wireMeshFromCurve(oneNodePerCurve=True)
```

## Examples
![Example 1 / v0.2](https://user-images.githubusercontent.com/13516657/35197776-1f40e718-fee5-11e7-9204-3dfaed3955e2.png "Example 1 / v0.2")

## License
As of now this project does not have any license, so the [default applies](https://choosealicense.com/no-license/#for-users), with one exception that you can use this software as a plugin inside of Autodesk Maya. This will change when version 1.0 hit (which should be in 2018) and I will choose one of free open-source licenses. With that being said, for the time being, any suggestions, opinions, feature request and bug reports are more than welcome.