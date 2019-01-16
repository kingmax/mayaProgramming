# coding:utf-8
# set transformation using Maya API 2.0
from maya.api import OpenMaya as om

selList = om.MGlobal.getActiveSelectionList()
dagPath = selList.getDagPath(0)
print(dagPath.fullPathName())

transformFn = om.MFnTransform(dagPath)
transformFn.setTranslation(om.MVector(1,2,3), om.MSpace.kTransform)
transformFn.translateBy(om.MVector(-1,0,0), om.MSpace.kTransform)

transformFn.setScale((1,0.5,0.8))
transformFn.scaleBy((0.5, 0.5, 0.5))

transformFn.setShear((0.5, 0, 0))
transformFn.shearBy((3, 0, 0))

import math
dir(math)
q = om.MQuaternion(math.radians(45), om.MVector(1,0,0))
print(q.x, q.y, q.z, q.w)
# (0.3826834323650898, 0.0, 0.0, 0.9238795325112867)
q2 = om.MQuaternion(math.radians(35), om.MVector(1,0,0))
transformFn.setRotation(q, om.MSpace.kTransform)
transformFn.rotateBy(q2, om.MSpace.kTransform)
# om.MSpace.kTransform == 1
transformFn.setRotation(om.MEulerRotation(math.radians(45), 0, 0), 1)
transformFn.rotateBy(om.MEulerRotation(math.radians(35), 0, 0), 1)

