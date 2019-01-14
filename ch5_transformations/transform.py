# coding:utf-8
# transform Point
from maya import OpenMaya as om

mat = om.MMatrix()
p0 = om.MPoint(1,2,3)
p1 = p0 * mat;
type(p1)
print(p1.x, p1.y, p1.z)

v = om.MVector(4,5,6)
v1 = v * mat;
print(v1.x, v1.y, v1.z)

mat2 = om.MMatrix()
v1 *= mat2;
print(v1.x, v1.y, v1.z)