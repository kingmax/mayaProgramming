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
    
    transformFn.getShear(scaleDoubleArrayPtr)
    x = om.MScriptUtil().getDoubleArrayItem(scaleDoubleArrayPtr, 0)
    y = om.MScriptUtil().getDoubleArrayItem(scaleDoubleArrayPtr, 1)
    z = om.MScriptUtil().getDoubleArrayItem(scaleDoubleArrayPtr, 2)
    print(x, y, z)
    
    quaternion = om.MQuaternion()
    transformFn.getRotation(quaternion)
    print(quaternion.x, quaternion.y, quaternion.z, quaternion.w)
    
    euler = om.MEulerRotation()
    transformFn.getRotation(euler)
    print(euler.x, euler.y, euler.z)
    
    # ERROR, maybe only in C++? because the RotationOrder is Enum in MTransformationMatrix class
    # order = om.MTransformationMatrix.RotationOrder() 
    # transformFn.getRotation(scaleDoubleArrayPtr, order)
    
    vector = om.MVector()
    vector = transformFn.translation(om.MSpace.kTransform)
    print(vector.x, vector.y, vector.z)
    
    ror = om.MQuaternion()
    ror = transformFn.rotateOrientation(om.MSpace.kTransform)
    print(ror.x, ror.y, ror.z, ror.w)
    
    # om.MTransformztionMatrix.RotationOrder
    order = transformFn.rotationOrder()
    print(order)
    # Result: 1 # 
    
    sp = transformFn.scalePivot(om.MSpace.kTransform)
    rp = transformFn.rotatePivot(om.MSpace.kTransform)
    print((sp.x, sp.y, sp.z), (rp.x, rp.y, rp.z))
    
    # scale and rotation pivot point translation
    spt = transformFn.scalePivotTranslation(om.MSpace.kTransform)
    rpt = transformFn.rotatePivotTranslation(om.MSpace.kTransform)
    print((spt.x, spt.y, spt.z), (rpt.x, rpt.y, rpt.z))
    
    # MTransformationMatrix
    tx = transformFn.transformation()
    print(tx)
    
    iter.next()