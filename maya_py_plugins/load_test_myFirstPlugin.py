import maya.cmds as cmds

f = r'D:\git\MayaProgramming\maya_py_plugins\myFirstPlugin.py'
try:
    cmds.unloadPlugin('myFirstPlugin.py')
except:
    pass
    
cmds.loadPlugin(f)

cmds.spHelloWorld()

