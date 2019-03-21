#-------------------------------------------------------------------------#
#   CREATED:
#       14 VIII 2017
#   INFO:
#       ...
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
#   IMPORTS
#-------------------------------------------------------------------------#
from maya.api.OpenMaya import   MGlobal

from maya.api.OpenMaya import   MFnPlugin
import maya.OpenMayaMPx as      oldOMMpx 

from maya.api.OpenMaya import   MPxData
from maya.api.OpenMaya import   MPxNode

import maya.cmds as cmds
import pymel.core as pm

#import wiresrc.wireProfileData; reload(wiresrc.wireProfileData)                     # ONLY FOR TESTING
from wiresrc.wireProfileData import WireProfileData
#import wiresrc.wireMeshFromCurveCommand; reload(wiresrc.wireMeshFromCurveCommand)   # ONLY FOR TESTING
from wiresrc.wireMeshFromCurveCommand import WireMeshFromCurveCommand
#import wiresrc.wireMeshCreatorNode; reload(wiresrc.wireMeshCreatorNode)             # ONLY FOR TESTING
from wiresrc.wireMeshCreatorNode import WireMeshCreatorNode
import wiresrc.aeWireMeshCreatorTemplate

#-------------------------------------------------------------------------#
#   GLOBALS
#-------------------------------------------------------------------------#
g_wireToolsMenuItemID = ""

#-------------------------------------------------------------------------#
#   FUNCTION DEFINITIONS
#   MAYA USE NEW API
#-------------------------------------------------------------------------#
def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """

    pass

#-------------------------------------------------------------------------#
#   INITIALIZE PLUGIN
#-------------------------------------------------------------------------#
def initializePlugin(mObj):
    fnPlugin = MFnPlugin(mObj, "Piotr Makal", "0.2.1", "Any")

    #-------------------------------------------------------------------------#
    #   INITIALIZATION CODE
    #-------------------------------------------------------------------------#
    # ADD MENU ITEM (WIRE TOOLS)
    global g_wireToolsMenuItemID
    try:
        # build Maya's Create menu
        # Since Maya doesn't build menus (their contents) on startup but rather
        # on demand (when user clicks specific menu) we need to invoke special
        # MEL procedure to make sure our menu item will be added when plugin is
        # loaded but user still haven't clicked on a specific menu (i.e. Create menu).
        parentMenu = pm.melGlobals["$gMainCreateMenu"]
        pm.mel.eval("ModCreateMenu " + parentMenu)  # MAYA_LOCATION/scripts/startup

        # check for possible insert positions
        menuItemList = cmds.menu(parentMenu, itemArray=True, query=True)
        if "createCurveTools" in menuItemList:
            insertAfterMenuItem = "createCurveTools"
        else:
            insertAfterMenuItem = menuItemList[6]   # more or less the position I want

        # add menu item with submenu
        g_wireToolsMenuItemID = cmds.menuItem(
            "wireTools", 
            label =         "Wire Tools",
            parent =        parentMenu,
            insertAfter =   insertAfterMenuItem,
            subMenu =       True,
            tearOff =       True
        )

        # add nested menu items
        # I'm using old API addMenuItem method because: (1) new API 2.0 does not 
        # have it; (2) using cmds.menuItem to add menu item will result in situation
        # in which you click on menu item holding Ctrl+Shift to add it to shelf as 
        # a button and Maya will attach pointer to Python function instead of actual 
        # Python command when button on the shelf is clicked - this will cause Maya 
        # to lose track of that pointer next time Maya is opened and clicking that 
        # button on the shelf will cause warning/error and nothing else.
        oldFnPlugin = oldOMMpx.MFnPlugin()
        oldFnPlugin.addMenuItem(
            "Wire Mesh from Curve",
            g_wireToolsMenuItemID,
            WireMeshFromCurveCommand.commandName,
            "-oneNodePerCurve false",
            False,
            "",
            "-image \"shelf_wireMeshFromCurve.png\""
        )

    except:
        if (g_wireToolsMenuItemID != ""):
            cmds.deleteUI(g_wireToolsMenuItemID, menuItem=True)
            g_wireToolsMenuItemID = ""

        MGlobal.displayWarning("Could not add Wire Tools menu item to Maya's Create menu.")

    #-------------------------------------------------------------------------#
    #   DATA
    #-------------------------------------------------------------------------#
    # WIRE PROFILE DATA
    wireProfileDataRegistrationFlag = True
    try:
        fnPlugin.registerData(
            WireProfileData.dataName,
            WireProfileData.dataID,
            WireProfileData.dataCreator,
            MPxData.kData
        )
    except:
        MGlobal.displayError("Failed to register " + WireProfileData.dataName 
            + " data!")
        wireProfileDataRegistrationFlag = False

    #-------------------------------------------------------------------------#
    #   COMMANDS
    #-------------------------------------------------------------------------#
    # WIRE MESH FROM CURVE
    try:
        fnPlugin.registerCommand(
            WireMeshFromCurveCommand.commandName,
            WireMeshFromCurveCommand.commandCreator,
            WireMeshFromCurveCommand.commandSyntax
        )
    except:
        MGlobal.displayError("Failed to register " + WireMeshFromCurveCommand.commandName 
            + " command!")

    #-------------------------------------------------------------------------#
    #   NODES
    #-------------------------------------------------------------------------#
    # WIRE MESH CREATOR NODE
    if (wireProfileDataRegistrationFlag == True):
        try:
            fnPlugin.registerNode(
                WireMeshCreatorNode.nodeName,
                WireMeshCreatorNode.nodeID,
                WireMeshCreatorNode.nodeCreator,
                WireMeshCreatorNode.nodeInitializer,
                MPxNode.kDependNode
            )
        except:
            MGlobal.displayError("Failed to register " + WireMeshCreatorNode.nodeName 
                + " node!")

    else:
        MGlobal.displayError("Because " + WireProfileData.dataName
            + " data failed to be registered, " + WireMeshCreatorNode.nodeName
            + " node also can not be registered.")

#-------------------------------------------------------------------------#
#   UNINITIALIZE PLUGIN
#-------------------------------------------------------------------------#
def uninitializePlugin(mObj):
    fnPlugin = MFnPlugin(mObj)

    #-------------------------------------------------------------------------#
    #   CLEANUP
    #-------------------------------------------------------------------------#
    # DELETE WIRE TOOLS MENU ITEM
    global g_wireToolsMenuItemID
    if (g_wireToolsMenuItemID != ""):
        cmds.deleteUI(g_wireToolsMenuItemID, menuItem=True)

    #-------------------------------------------------------------------------#
    #   DATA
    #-------------------------------------------------------------------------#
    # WIRE PROFILE DATA
    try:
        fnPlugin.deregisterData(WireProfileData.dataID)
    except:
        MGlobal.displayError("Failed to deregister " + WireProfileData.dataName 
            + " data!")

    #-------------------------------------------------------------------------#
    #   COMMANDS
    #-------------------------------------------------------------------------#
    # WIRE MESH FROM CURVE
    try:
        fnPlugin.deregisterCommand(WireMeshFromCurveCommand.commandName)
    except:
        MGlobal.displayError("Failed to deregister " + WireMeshFromCurveCommand.commandName 
            + " command!")

    #-------------------------------------------------------------------------#
    #   NODES
    #-------------------------------------------------------------------------#
    # WIRE MESH CREATOR NODE
    try:
        fnPlugin.deregisterNode(WireMeshCreatorNode.nodeID)
    except:
        MGlobal.displayError("Failed to deregister " + WireMeshCreatorNode.nodeName 
            + " node!")
