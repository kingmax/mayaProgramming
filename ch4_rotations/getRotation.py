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

