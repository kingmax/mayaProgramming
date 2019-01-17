# coding:utf-8

# mel
# upAxis -q -axis;
# setUpAxis "z";

from maya.api import OpenMaya as om
from maya import OpenMaya as oom

yIsUp = om.MGlobal.isYAxisUp()
up = om.MGlobal.upAxis()
om.MGlobal.setZAxisUp(True)
