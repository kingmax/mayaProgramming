# coding:utf-8
# get transformation matrix using maya python api 2.0
from maya.api import OpenMaya as om

#selList = om.MGlobal.getSelectionListByName('*')
selList = om.MGlobal.getActiveSelectionList()
print(selList.length())
# help(om.MItSelectionList)
it = om.MItSelectionList(selList)
while not it.isDone():
    try:
        dagPath = it.getDagPath()
        print(dagPath.fullPathName())
        
        obj2ws = dagPath.inclusiveMatrix()
        print('object to world:')
        print(obj2ws)
        ws2obj = dagPath.inclusiveMatrixInverse()
        print('world to object:')
        print(ws2obj)
        
        print('\r\nthe Parent space:')
        pObj2WS = dagPath.exclusiveMatrix()
        print('object to world:')
        print(pObj2WS)
        pWS2Obj = dagPath.exclusiveMatrixInverse()
        print('world to object:')
        print(pWS2Obj)
        
        # child
        if dagPath.childCount() < selList.length():
            print('-' * 40)
            print(dagPath.fullPathName())
            mObj2WS = dagPath.inclusiveMatrix()
            mParentWS2Obj = dagPath.exclusiveMatrixInverse()
            matrix = mObj2WS * mParentWS2Obj
            print(matrix)
    except:
        pass
    print('\r\n')
    it.next()