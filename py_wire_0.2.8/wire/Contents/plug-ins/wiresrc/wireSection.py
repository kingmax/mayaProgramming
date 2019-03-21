#-------------------------------------------------------------------------#
#   CREATED:
#       28 VIII 2017
#   INFO:
#       WireSection is in most basic scenario a WireProfileData but in 
#       world space (has model matrix). It can be translated, rotated and
#       scaled.
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
#   IMPORTS
#-------------------------------------------------------------------------#
from maya.api.OpenMaya import MGlobal
from maya.api.OpenMaya import MPoint
from maya.api.OpenMaya import MQuaternion
from maya.api.OpenMaya import MSpace
from maya.api.OpenMaya import MTransformationMatrix
from maya.api.OpenMaya import MVector

from wiresrc.wireProfileData import WireProfileData

#-------------------------------------------------------------------------#
#   CLASS DEFINITIONS
#   WIRE SECTION
#-------------------------------------------------------------------------#
class WireSection(object):
    #-------------------------------------------------------------------------#
    #   TYPES
    #-------------------------------------------------------------------------#
    class RotationType:
        ALIGN_WITH_TANGENT =        0
        ADJUST_ON_EP =              1
        CUSTOM_PROFILE_ROTATION =   2
        TWIST =                     3

    #-------------------------------------------------------------------------#
    #   CONSTRUCTOR
    #   (WireProfileData)
    #-------------------------------------------------------------------------#
    def __init__(self, wireProfileData):
        # INITIALIZE
        self.wireProfileData =              wireProfileData
        self.isWireProfileDataModified =    False
        self.modelMatrix =                  MTransformationMatrix()
        self.rotationMap =                  {}

    #-------------------------------------------------------------------------#
    #   SET TRANSLATION
    #-------------------------------------------------------------------------#
    def setTranslation(self, point):
        self.modelMatrix.setTranslation(MVector(point), MSpace.kTransform)

    #-------------------------------------------------------------------------#
    #   SET ROTATION
    #-------------------------------------------------------------------------#
    def setRotation(self, rotation):
        """
        Rotation paramater may be either MQuaternion or MEulerRotation
        """
        self.modelMatrix.setRotation(rotation)

    #-------------------------------------------------------------------------#
    #   SET SCALE
    #-------------------------------------------------------------------------#
    def setScale(self, scaleX, scaleY, scaleZ):
        self.modelMatrix.setScale((scaleX, scaleY, scaleZ), MSpace.kTransform)

    #-------------------------------------------------------------------------#
    #   GET ROTATION
    #-------------------------------------------------------------------------#
    def getRotation(self, asQuaternion=True):
        return self.modelMatrix.rotation(asQuaternion)

    #-------------------------------------------------------------------------#
    #   GET ROTATION OF TYPE
    #-------------------------------------------------------------------------#
    def getRotationOfType(self, rotationType):
        """
        rotationType parameter refers to "enumerator" which is RotationType class.
        """
        try:
            rotation = self.rotationMap[rotationType]
        except:
            rotation = MQuaternion()
        
        return rotation

    #-------------------------------------------------------------------------#
    #   GET LOCAL X AXIS
    #-------------------------------------------------------------------------#
    def getLocalXAxis(self):
        return MVector(1.0, 0.0, 0.0) * self.modelMatrix.asMatrix()

    #-------------------------------------------------------------------------#
    #   GET LOCAL Y AXIS
    #-------------------------------------------------------------------------#
    def getLocalYAxis(self):
        return MVector(0.0, 1.0, 0.0) * self.modelMatrix.asMatrix()

    #-------------------------------------------------------------------------#
    #   GET LOCAL Z AXIS
    #-------------------------------------------------------------------------#
    def getLocalZAxis(self):
        return MVector(0.0, 0.0, 1.0) * self.modelMatrix.asMatrix()

    #-------------------------------------------------------------------------#
    #   GET SUBPROFILE POINTS
    #-------------------------------------------------------------------------#
    def getSubprofilePoints(self, index):
        """
        Returns subprofile points in world space.
        """
        if self.isWireProfileDataModified == True:
            wireProfileData = self.wireProfileDataModified
        else:
            wireProfileData = self.wireProfileData
        
        pointInLocalSpaceList = wireProfileData.getSubprofilePoints(index)
        pointInWorldSpaceList = []
        
        for pointInLocalSpace in pointInLocalSpaceList:
            pointInWorldSpace = pointInLocalSpace * self.modelMatrix.asMatrix()
            pointInWorldSpaceList.append(pointInWorldSpace)

        return pointInWorldSpaceList

    #-------------------------------------------------------------------------#
    #   ROTATE
    #-------------------------------------------------------------------------#
    def rotate(self, rotation, rotationType):
        """
        Rotation paramater may be either MQuaternion or MEulerRotation.
        rotationType parameter refers to "enumerator" which is RotationType class.
        """
        self.modelMatrix.rotateBy(rotation, MSpace.kTransform)
        self.rotationMap[rotationType] = rotation

    #-------------------------------------------------------------------------#
    #   SCALE ALONG VECTOR
    #-------------------------------------------------------------------------#
    def scaleAlongVector(self, scaleValue, scaleDirectionVector):
        """
        For proper results this method assumes that scaleDirectionVector is 
        on the same plane as WireSection (in world space).
        """

        self.isWireProfileDataModified =    True
        self.wireProfileDataModified =      WireProfileData(self.wireProfileData.getSubprofileList())

        scaleDirectionVectorLocalSpace = scaleDirectionVector * self.modelMatrix.asMatrixInverse()
        scaleDirectionVectorLocalSpace.z = 0.0

        if (scaleDirectionVectorLocalSpace != MVector(0.0, 0.0, 0.0)):
            self.wireProfileDataModified.scaleAlongVector(
                scaleValue, scaleDirectionVectorLocalSpace)
        else:
            MGlobal.displayWarning("Could not scale wire section along provided vector.")


