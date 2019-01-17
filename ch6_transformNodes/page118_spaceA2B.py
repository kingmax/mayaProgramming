# coding:utf-8
# determine the object space coordinates of a point given any other space£¬ page118
from maya.api import OpenMaya as om

selection = om.MSelectionList()
selection.add('objA')
print(selection.length())
selection.add('objB')
print(selection.length())

a = selection.getDagPath(0)
type(a)
# Result: <type 'OpenMaya.MDagPath'> # 
matA_Obj2WS = a.inclusiveMatrix()

b = selection.getDagPath(1)
matB_WS2Obj = b.inclusiveMatrixInverse()

pt = om.MPoint(0, 0, 0)
pt *= matA_Obj2WS * matB_WS2Obj
print(pt)

from maya import cmds
cmds.spaceLocator(p=(pt.x, pt.y, pt.z))
cmds.sphere(p=(pt.x, pt.y, pt.z))

