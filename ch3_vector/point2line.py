# coding:utf-8
# calculate vector(point) perpendicular to line(pointB-pointA)
# trans from C++

from maya import OpenMaya as om

p = om.MPoint(1,3,4)
p0 = om.MPoint(0,0,0)
p1 = om.MPoint(1,0,0)

a = p - p0
type(a)
type(p)
b = p1 - p0
b.normalize()
#c = (a * b)*b ##ERROR
c = b * (a * b)
d = a - c
om.MGlobal.displayInfo('distance: %s'%d.length())
