#-------------------------------------------------------------------------#
#   CREATED:
#		05 IX 2017
#   INFO:
#       ...
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
#   IMPORTS
#-------------------------------------------------------------------------#
import math
from maya.api.OpenMaya import MPoint

#-------------------------------------------------------------------------#
#   FUNCTION DEFINITIONS
#   DOT
#-------------------------------------------------------------------------#
def dot(vectorA, vectorB):
    """
    Calculates dot product of two vectors.
    """
    result = 0.0

    # CHECK
    if len(vectorA) != len(vectorB):
        return result

    # CALCULATE
    for i in range(len(vectorA)):
        result += vectorA[i] * vectorB[i]

    return result

#-------------------------------------------------------------------------#
#   CREATE POLYGON POINT LIST
#-------------------------------------------------------------------------#
def createPolygonPointList(numSides, radius=1.0):
    """
    Returns list of MPoints representing n-sided polygon placed on xy plane.
    """
    radianSteps =   math.radians(360.0 / numSides)
    pointList =     []

    for i in range(numSides):
        x = round(math.cos(radianSteps * i), 7) * radius
        y = round(math.sin(radianSteps * i), 7) * radius

        # Rotate point by 90 degrees so first is always placed with coordinates
        # x = 0 and y = 1 instead of x = 1 and y = 0 - this is approach that
        # most users may be familiar with from math lessons when drawing polygons.
        angle = math.pi/2   # 90 degrees
        x90 = x * math.cos(angle) - y * math.sin(angle)
        y90 = y * math.cos(angle) + x * math.sin(angle)

        pointList.append(MPoint(x90, y90, 0.0))

    return pointList
