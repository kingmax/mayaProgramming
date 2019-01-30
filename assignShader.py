# coding:utf-8
# assign a shader to obj
# ref: https://forums.cgsociety.org/t/python-how-to-assign-a-material-to-an-object/1459648/4

from maya import cmds

obj = cmds.polyCube()[0]
shader = cmds.shadingNode('lambert', asShader=True, name='myShader')
cmds.setAttr('%s.color'%shader, 1, 0, 0)
cmds.select(obj)
cmds.hyperShade(assign=shader)

# method 2:
    
sphereObj = cmds.polySphere()[0]
cmds.move(10, 0, 0, sphereObj, r=True, ws=True)
shader2 = cmds.shadingNode('blinn', asShader=True, n='myBlinn')
cmds.setAttr('%s.color'%shader2, 0, 1, 0)
shadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, n='%sSG'%shader2)
cmds.connectAttr('%s.outColor'%shader2, '%s.surfaceShader'%shadingGroup)
cmds.sets(sphereObj, edit=True, forceElement=shadingGroup)