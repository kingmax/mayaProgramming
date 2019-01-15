# coding:utf-8
# query transformation using maya API
from maya import OpenMaya as om

selList = om.MSelectionList()
om.MGlobal.getActiveSelectionList(selList)
iter = om.MItSelectionList(selList)
dagPath = om.MDagPath()
s = list()
while not iter.isDone():
    iter.getDagPath(dagPath)
    #dagPath.fullPathName()
    transformFn = om.MFnTransform(dagPath)
    #transformFn.getScale(s) #Type ERROR
    #ref: http://forums.cgsociety.org/t/api-getscale-method-in-python/1301482/2
    scaleDoubleArray = om.MScriptUtil()
    scaleDoubleArray.createFromList([0.0, 0.0, 0.0], 3)
    scaleDoubleArrayPtr = scaleDoubleArray.asDoublePtr()
    type(scaleDoubleArrayPtr)
    transformFn.getScale(scaleDoubleArrayPtr)
    sx = om.MScriptUtil().getDoubleArrayItem(scaleDoubleArrayPtr, 0)
    sy = om.MScriptUtil().getDoubleArrayItem(scaleDoubleArrayPtr, 1)
    sz = om.MScriptUtil().getDoubleArrayItem(scaleDoubleArrayPtr, 2)
    print(sx, sy, sz)
    iter.next()