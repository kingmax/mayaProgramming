from maya import OpenMaya as om
import math

dagPath = om.MDagPath()
selectionList = om.MSelectionList()
om.MGlobal.getActiveSelectionList(selectionList)

for i in range(selectionList.length()):
    selectionList.getDagPath(i, dagPath)
    print(dagPath.fullPathName())
    
    transformFn = om.MFnTransform(dagPath)
    stat = 0
    er = om.MEulerRotation()
    transformFn.getRotation(er)
    print('rotation: %s, %s, %s, order:%s'%(er.x, er.y, er.z, er.order))
    
    # another method, ref: https://www.akeric.com/blog/?p=1067
    matrix = transformFn.transformation()
    eulerRot = matrix.eulerRotation()
    print(eulerRot.y)
    math.degrees(eulerRot.y)
    angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
    print(angles, "MTransformationMatrix")
    
    # set the absolute rotation
    rot = om.MEulerRotation(0, math.radians(30), 0)
    transformFn.setRotation(rot)
    # add a relative rotation
    rotOffset = om.MEulerRotation(0, math.radians(15), 0)
    transformFn.rotateBy(rotOffset)

# 

'''
from maya import OpenMaya as om

selList = om.MSelectionList()
om.MGlobal.getActiveSelectionList(selList)
selList.length()
dagPath = om.MDagPath()
for i in range(selList.length()):
    selList.getDagPath(i, dagPath)
    print(dagPath.fullPathName())
    transformFn = om.MFnTransform(dagPath)
    er = om.MEulerRotation()
    transformFn.getRotation(er)
    print('rotation: %s, %s, %s, order:%s'%(er.x, er.y, er.z, er.order))
'''
