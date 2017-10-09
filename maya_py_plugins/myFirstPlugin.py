#!/usr/bin/env python
#coding:utf-8
"""
  Author:  iJasonLee (kingmax_res@163.com | 184327932@qq.com)
  Purpose: #first maya python plug-in
  Created: 2017/10/9
"""
#file:///D:/2017.6.6/sdk_help/maya-2014-sdk-doc0/index.html

import os
import sys
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginCmdName = 'spHelloWorld'
kPluginVendor  = '184327932@qq.com'
kPluginVersion = '2017.10.09.01'

#Menu and Shelf
########################################################################
#----------------------------------------------------------------------
def makeMenu(menuName='iQA'):
    """"""
    removeMenu(menuName)
    #http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/CommandsPython/window.html
    topMenu = cmds.menu(menuName, label=menuName, parent=u'MayaWindow', tearOff=True)
    cmds.menuItem(label='Hello World', parent=topMenu, command=kPluginCmdName, sourceType='mel')
    
#----------------------------------------------------------------------
def removeMenu(menuName='iQA'):
    """"""
    if cmds.menu(menuName, q=True, exists=True):
        cmds.deleteUI(menuName, menu=True)
        
#----------------------------------------------------------------------
def makeShelf(shelfName='iQA'):
    """"""
    #http://forums.cgsociety.org/archive/index.php?t-1091198.html
    test = cmds.shelfLayout(shelfName, exists=True)
    if test:
        newShelf = shelfName
        buttons = cmds.shelfLayout(shelfName, q=True, childArray=True)
        if buttons:
            for btn in buttons:
                cmds.deleteUI(btn, control=True)
    else:
        newShelf = mel.eval('addNewShelfTab("%s")'%shelfName)
    cmds.setParent(newShelf)
    cmds.shelfButton(label=kPluginCmdName, annotation=kPluginCmdName, sourceType='python', command='import maya.cmds as cmds;\ncmds.spHelloWorld()', image='pythonFamily.png', imageOverlayLabel=shelfName)
    
#----------------------------------------------------------------------
def removeShelf(shelfName='iQA'):
    """"""
    test = cmds.shelfLayout(shelfName, exists=True)
    if test:
        mel.eval('deleteShelfTab %s'%shelfName)
        gShelfTopLevel = mel.eval('$tempVar=$gShelfTopLevel')
        cmds.saveAllShelves(gShelfTopLevel)
########################################################################        


#Command
########################################################################
class scriptedCommand(OpenMayaMPx.MPxCommand):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        super(scriptedCommand, self).__init__()
        
    #----------------------------------------------------------------------
    def doIt(self, argList):
        """Invoke when the command is run"""
        print('Hello World!')
        

#Creator
#----------------------------------------------------------------------
def cmdCreator():
    """Creator"""
    return OpenMayaMPx.asMPxPtr(scriptedCommand())


#Initialize the script plug-in
#----------------------------------------------------------------------
def initializePlugin(mobject):
    """Initialize the script plug-in"""
    mplugin = OpenMayaMPx.MFnPlugin(mobject, kPluginVendor, kPluginVersion)
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator)
        makeMenu(menuName='iQA')
        makeShelf(shelfName='iQA')
    except:
        sys.stderr.write('Failed to register command: %s\n'%kPluginCmdName)
        raise
    
#Uninitialize the script plug-in
#----------------------------------------------------------------------
def uninitializePlugin(mobject):
    """Uninitialize the script plug-in"""
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
        removeMenu(menuName='iQA')
        removeShelf(shelfName='iQA')
    except:
        sys.stderr.write('Failed to unregister command: %s\n'%kPluginCmdName)  