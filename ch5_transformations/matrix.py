# coding:utf-8
# MMatrix api
from maya import OpenMaya as om

mat = om.MMatrix()
mat.setToIdentity()

def printMatrix(mat):
    for i in range(4):
        row = ''
        for j in range(4):
            value = mat(i, j)
            row += '%s, '%value
        print(row)
    
fm = om.MFloatMatrix()
fm.get(mat.matrix)
dm = om.MMatrix()
dm.get(fm.matrix)

inv = dm.inverse()
type(inv) # Result: <class 'maya.OpenMaya.MMatrix'> # 
printMatrix(inv)

trans = dm.transpose()
printMatrix(trans)