# coding:utf-8
# using Maya Python API 2.0
from maya.api import OpenMaya as om
import math

def maya_useNewAPI():
    pass

selList = om.MGlobal.getActiveSelectionList()

iter = om.MItSelectionList(selList)
while not iter.isDone():
    dagPath = iter.getDagPath()
    print(dagPath.fullPathName())
    transformFn = om.MFnTransform(dagPath)
    eulerRot   = transformFn.rotation()
    print(math.degrees(eulerRot.y))
    quaternion = transformFn.rotation(asQuaternion=True)
    print(quaternion)
    
    # set the absolute rotation of an object
    r = om.MQuaternion(math.radians(10), om.MVector(0, 1, 0))
    transformFn.setRotation(r, om.MSpace.kWorld)
    
    # add a relative rotation to an existing rotation
    r2 = om.MQuaternion(math.radians(20), om.MVector(0, 1, 0))
    transformFn.rotateBy(r2, om.MSpace.kWorld)
    
    # quaternion concatenation
    q = transformFn.rotation(asQuaternion = True)
    r3 = om.MQuaternion(math.radians(15), om.MVector(0,1,0))
    q *= r3
    transformFn.setRotation(q, om.MSpace.kWorld)
    # now 45 degrees
    
    iter.next()
    