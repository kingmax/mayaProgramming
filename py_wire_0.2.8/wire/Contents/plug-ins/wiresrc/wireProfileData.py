#-------------------------------------------------------------------------#
#   CREATED:
#       27 VIII 2017
#   INFO:
#       ...
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
#   IMPORTS
#-------------------------------------------------------------------------#
import math

from maya.api.OpenMaya import MTypeId
from maya.api.OpenMaya import MVector

from maya.api.OpenMaya import MPxData

#-------------------------------------------------------------------------#
#   CLASS DEFINITIONS
#   WIRE PROFILE DATA
#-------------------------------------------------------------------------#
class WireProfileData(MPxData):
    #-------------------------------------------------------------------------#
    #   STATIC CLASS MEMBERS
    #-------------------------------------------------------------------------#
    # DATA INFORMATIONS
    dataID =        MTypeId(0x0012bc81)
    dataName =      "wireProfileData"

    #-------------------------------------------------------------------------#
    #   CONSTRUCTOR
    #   ([WireSubprofile, ...])
    #-------------------------------------------------------------------------#
    def __init__(self, subprofileList, *args, **kwargs):
        # INITIALIZE
        super(WireProfileData, self).__init__(*args, **kwargs)
        self.subprofileList = subprofileList

    #-------------------------------------------------------------------------#
    #   IS SUBPROFILE CLOSED
    #-------------------------------------------------------------------------#
    def isSubprofileClosed(self, index):
        return self.subprofileList[index].isClosed()

    #-------------------------------------------------------------------------#
    #   GET SUBPROFILE LIST
    #-------------------------------------------------------------------------#
    def getSubprofileList(self):
        return self.subprofileList

    #-------------------------------------------------------------------------#
    #   GET NUMBER OF SUBPROFILES
    #-------------------------------------------------------------------------#
    def getNumSubprofiles(self):
        return len(self.subprofileList)

    #-------------------------------------------------------------------------#
    #   GET SUBPROFILE SIZE
    #-------------------------------------------------------------------------#
    def getSubprofileSize(self, index):
        return len(self.subprofileList[index].getPointList())

    #-------------------------------------------------------------------------#
    #   GET SUBPROFILE POINTS
    #-------------------------------------------------------------------------#
    def getSubprofilePoints(self, index):
        return self.subprofileList[index].getPointList()

    #-------------------------------------------------------------------------#
    #   SCALE ALONG VECTOR
    #-------------------------------------------------------------------------#
    def scaleAlongVector(self, scaleValue, scaleDirectionVector):
        """
        This method scales subrofiles along vector and bakes this scaling 
        information into subprofile points. 
        """

        scaleDirectionVector.normalize()

        newSubprofileList = []
        for subprofile in self.subprofileList:
            scaledPointList = []
            for point in subprofile.getPointList():
                pointVector = MVector(point)
                pointPrime = point + (
                    scaleDirectionVector 
                    * math.cos(pointVector.angle(scaleDirectionVector))
                    * pointVector.length()
                    * (scaleValue - 1.0))

                scaledPointList.append(pointPrime)

            newSubprofile = WireSubprofile(scaledPointList, subprofile.isClosed())
            newSubprofileList.append(newSubprofile)

        self.subprofileList = newSubprofileList

    #-------------------------------------------------------------------------#
    #   COPY
    #-------------------------------------------------------------------------#
    def copy(data):
        """
        This method can be thought of as the second half of a copy constructor 
        for the class. The default constructor has already been called for the 
        instance, and this method is used to set the private data by copying 
        the values from an existing instance.
        """
        pass

    #-------------------------------------------------------------------------#
    #   TYPE ID
    #-------------------------------------------------------------------------#
    def typeId():
        return WireProfileData.dataID

    #-------------------------------------------------------------------------#
    #   NAME
    #-------------------------------------------------------------------------#
    def name():
        return WireProfileData.dataName

    #-------------------------------------------------------------------------#
    #   DATA CREATOR
    #-------------------------------------------------------------------------#
    @staticmethod
    def dataCreator():
        return WireProfileData()

#-------------------------------------------------------------------------#
#   WIRE SUBPROFILE
#-------------------------------------------------------------------------#
class WireSubprofile(object):
    #-------------------------------------------------------------------------#
    #   CONSTRUCTOR
    #   ([MPoint, ...], bool)
    #-------------------------------------------------------------------------#
    def __init__(self, pointList, isClosed):
        self._pointList =   pointList
        self._isClosed =    isClosed

    #-------------------------------------------------------------------------#
    #   IS CLOSED
    #-------------------------------------------------------------------------#
    def isClosed(self):
        return self._isClosed

    #-------------------------------------------------------------------------#
    #   GET POINT LIST
    #-------------------------------------------------------------------------#
    def getPointList(self):
        return self._pointList
