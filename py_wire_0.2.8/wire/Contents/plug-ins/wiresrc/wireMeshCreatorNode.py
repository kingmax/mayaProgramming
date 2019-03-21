#-------------------------------------------------------------------------#
#   CREATED:
#       19 VIII 2017
#   INFO:
#       ...
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
#   IMPORTS
#-------------------------------------------------------------------------#
import math

import maya.api.OpenMaya as om

from maya.api.OpenMaya import MArrayDataHandle
from maya.api.OpenMaya import MDataBlock
from maya.api.OpenMaya import MDataHandle
from maya.api.OpenMaya import MEulerRotation
from maya.api.OpenMaya import MItMeshEdge
from maya.api.OpenMaya import MObject
from maya.api.OpenMaya import MPoint
from maya.api.OpenMaya import MPointArray
from maya.api.OpenMaya import MQuaternion
from maya.api.OpenMaya import MSpace
from maya.api.OpenMaya import MTransformationMatrix
from maya.api.OpenMaya import MTypeId
from maya.api.OpenMaya import MVector

from maya.api.OpenMaya import MFnData
from maya.api.OpenMaya import MFnDependencyNode
from maya.api.OpenMaya import MFnEnumAttribute
from maya.api.OpenMaya import MFnMesh
from maya.api.OpenMaya import MFnMeshData
from maya.api.OpenMaya import MFnNumericAttribute
from maya.api.OpenMaya import MFnNumericData
from maya.api.OpenMaya import MFnNurbsCurve
from maya.api.OpenMaya import MFnTypedAttribute

from maya.api.OpenMaya import MPxNode

import maya.cmds as cmds

import wiresrc.utils.mathUtils as mathUtils
#reload(mathUtils)                                                   # ONLY FOR TESTING
from wiresrc.wireProfileData import WireProfileData
from wiresrc.wireProfileData import WireSubprofile
#import wiresrc.wireSection; reload(wiresrc.wireSection)             # ONLY FOR TESTING
from wiresrc.wireSection import WireSection

#-------------------------------------------------------------------------#
#   CLASS DEFINITIONS
#   WIRE MESH CREATOR NODE BACKUP DATA
#-------------------------------------------------------------------------#
class WMCNBD(object):
    """
    Idea behind this class is that we copy attribute values from WireMeshCreatorNode
    and store them here. Each WireMeshCreatorNode has an instance of this class 
    that allows later comparison with current attribute values and based on that
    we can perform certain optimizations inside compute function of WireMeshCreatorNode.
    For example it would be costly to calculate new wire topology that is outputed
    from WireMeshCreatorNode every time we change ANY attribute (i.e. attribute
    that only change position of vertices).
    """

    #-------------------------------------------------------------------------#
    #   CONSTRUCTOR
    #-------------------------------------------------------------------------#
    def __init__(self):
        self.initialize = True

    #-------------------------------------------------------------------------#
    #   COMPARE DATA
    #-------------------------------------------------------------------------#
    def compareData(self, dataBlock, computeFlagMap):
        # INITIALIZE
        if self.initialize == True:
            self._initializeData(dataBlock)
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True
            return computeFlagMap

        # WIRE PROFILE
        if self.wireProfileIndex != dataBlock.inputValue(WireMeshCreatorNode.aWireProfileIndex).asShort():
            self.wireProfileIndex = dataBlock.inputValue(WireMeshCreatorNode.aWireProfileIndex).asShort()
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True

        # rpolygon wire profile
        if self.rPolygonType != dataBlock.inputValue(WireMeshCreatorNode.aRPolygonType).asShort():
            self.rPolygonType = dataBlock.inputValue(WireMeshCreatorNode.aRPolygonType).asShort()
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True

        if self.rPolygonSides != dataBlock.inputValue(WireMeshCreatorNode.aRPolygonSides).asInt():
            self.rPolygonSides = dataBlock.inputValue(WireMeshCreatorNode.aRPolygonSides).asInt()
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True

        if self.rPolygonInnerRadius != dataBlock.inputValue(WireMeshCreatorNode.aRPolygonInnerRadius).asFloat():
            self.rPolygonInnerRadius = dataBlock.inputValue(WireMeshCreatorNode.aRPolygonInnerRadius).asFloat()
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True

        # pattern
        if self.patternEnable != dataBlock.inputValue(WireMeshCreatorNode.aPatternEnable).asBool():
            self.patternEnable = dataBlock.inputValue(WireMeshCreatorNode.aPatternEnable).asBool()
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True

        if self.patternLayout != dataBlock.inputValue(WireMeshCreatorNode.aPatternLayout).asShort():
            self.patternLayout = dataBlock.inputValue(WireMeshCreatorNode.aPatternLayout).asShort()
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True

        if self.patternNOS != dataBlock.inputValue(WireMeshCreatorNode.aPatternNOS).asInt():
            self.patternNOS = dataBlock.inputValue(WireMeshCreatorNode.aPatternNOS).asInt()
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True

        if self.patternScaleSubprofiles != dataBlock.inputValue(WireMeshCreatorNode.aPatternScaleSubprofiles).asFloat():
            self.patternScaleSubprofiles = dataBlock.inputValue(WireMeshCreatorNode.aPatternScaleSubprofiles).asFloat()
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True

        if self.patternCoverage != dataBlock.inputValue(WireMeshCreatorNode.aPatternCoverage).asFloat():
            self.patternCoverage = dataBlock.inputValue(WireMeshCreatorNode.aPatternCoverage).asFloat()
            computeFlagMap["topology"] =        True
            computeFlagMap["wireProfile"] =     True
            computeFlagMap["normals"] =         True

        # INTERPOLATION
        if self.interpolationRange != dataBlock.inputValue(WireMeshCreatorNode.aInterpolationRange).asShort():
            self.interpolationRange = dataBlock.inputValue(WireMeshCreatorNode.aInterpolationRange).asShort()
            computeFlagMap["topology"] =        True
            computeFlagMap["normals"] =         True

        if self.interpolationSteps != dataBlock.inputValue(WireMeshCreatorNode.aInterpolationSteps).asInt():
            self.interpolationSteps = dataBlock.inputValue(WireMeshCreatorNode.aInterpolationSteps).asInt()
            computeFlagMap["topology"] =        True
            computeFlagMap["normals"] =         True

        if self.interpolationDistance != dataBlock.inputValue(WireMeshCreatorNode.aInterpolationDistance).asFloat():
            self.interpolationDistance = dataBlock.inputValue(WireMeshCreatorNode.aInterpolationDistance).asFloat()
            computeFlagMap["topology"] =        True
            computeFlagMap["normals"] =         True

        # TRANSFORMATIONS
        if self.scaleProfile != dataBlock.inputValue(WireMeshCreatorNode.aScaleProfile).asFloat():
            self.scaleProfile = dataBlock.inputValue(WireMeshCreatorNode.aScaleProfile).asFloat()

        if self.rotateProfile != dataBlock.inputValue(WireMeshCreatorNode.aRotateProfile).asFloat():
            self.rotateProfile = dataBlock.inputValue(WireMeshCreatorNode.aRotateProfile).asFloat()

        if self.twist != dataBlock.inputValue(WireMeshCreatorNode.aTwist).asFloat():
            self.twist = dataBlock.inputValue(WireMeshCreatorNode.aTwist).asFloat()

        # NORMALS
        if self.normalsReverse != dataBlock.inputValue(WireMeshCreatorNode.aNormalsReverse).asBool():
            self.normalsReverse = dataBlock.inputValue(WireMeshCreatorNode.aNormalsReverse).asBool()
            computeFlagMap["topology"] =        True
            computeFlagMap["normals"] =         True

        if self.normalsSmoothing != dataBlock.inputValue(WireMeshCreatorNode.aNormalsSmoothing).asFloat():
            self.normalsSmoothing = dataBlock.inputValue(WireMeshCreatorNode.aNormalsSmoothing).asFloat()
            computeFlagMap["normals"] =         True

        return computeFlagMap

    #-------------------------------------------------------------------------#
    #   _ INITIALIZE DATA
    #-------------------------------------------------------------------------#
    def _initializeData(self, dataBlock):
        self.interpolationRange =       dataBlock.inputValue(WireMeshCreatorNode.aInterpolationRange).asShort()
        self.interpolationSteps =       dataBlock.inputValue(WireMeshCreatorNode.aInterpolationSteps).asInt()
        self.interpolationDistance =    dataBlock.inputValue(WireMeshCreatorNode.aInterpolationDistance).asFloat()
        self.normalsReverse =           dataBlock.inputValue(WireMeshCreatorNode.aNormalsReverse).asBool()
        self.normalsSmoothing =         dataBlock.inputValue(WireMeshCreatorNode.aNormalsSmoothing).asFloat()
        self.patternCoverage =          dataBlock.inputValue(WireMeshCreatorNode.aPatternCoverage).asFloat()
        self.patternEnable =            dataBlock.inputValue(WireMeshCreatorNode.aPatternEnable).asBool()
        self.patternLayout =            dataBlock.inputValue(WireMeshCreatorNode.aPatternLayout).asShort()
        self.patternNOS =               dataBlock.inputValue(WireMeshCreatorNode.aPatternNOS).asInt()
        self.patternScaleSubprofiles =  dataBlock.inputValue(WireMeshCreatorNode.aPatternScaleSubprofiles).asFloat()
        self.rotateProfile =            dataBlock.inputValue(WireMeshCreatorNode.aRotateProfile).asFloat()
        self.rPolygonInnerRadius =      dataBlock.inputValue(WireMeshCreatorNode.aRPolygonInnerRadius).asFloat()
        self.rPolygonSides =            dataBlock.inputValue(WireMeshCreatorNode.aRPolygonSides).asInt()
        self.rPolygonType =             dataBlock.inputValue(WireMeshCreatorNode.aRPolygonType).asShort()
        self.scaleProfile =             dataBlock.inputValue(WireMeshCreatorNode.aScaleProfile).asFloat()
        self.twist =                    dataBlock.inputValue(WireMeshCreatorNode.aTwist).asFloat()
        self.wireProfileIndex =         dataBlock.inputValue(WireMeshCreatorNode.aWireProfileIndex).asShort()

        self.initialize =               False

#-------------------------------------------------------------------------#
#   WIRE MESH CREATOR NODE
#-------------------------------------------------------------------------#
class WireMeshCreatorNode(MPxNode):
    #-------------------------------------------------------------------------#
    #   STATIC CLASS MEMBERS
    #-------------------------------------------------------------------------#
    # NODE INFORMATIONS
    nodeID =                    MTypeId(0x0012bc80)
    nodeName =                  "wireMeshCreator"

    # ATTRIBUTES
    aCustomWireProfileData =    MObject();  anCustomWireProfileData =   "customWireProfileData"
    aInCurveArray =             MObject();  anInCurveArray =            "inCurveArray"
    aInterpolationDistance =    MObject();  anInterpolationDistance =   "interpolationDistance"
    aInterpolationRange =       MObject();  anInterpolationRange =      "interpolationRange"
    aInterpolationSteps =       MObject();  anInterpolationSteps =      "interpolationSteps"
    aNormalsReverse =           MObject();  anNormalsReverse =          "normalsReverse"
    aNormalsSmoothing =         MObject();  anNormalsSmoothing =        "normalsSmoothing"
    aOutMeshArray =             MObject();  anOutMeshArray =            "outMeshArray"
    aPatternCoverage =          MObject();  anPatternCoverage =         "patternCoverage"
    aPatternEnable =            MObject();  anPatternEnable =           "patternEnable"
    aPatternLayout =            MObject();  anPatternLayout =           "patternLayout"
    aPatternNOS =               MObject();  anPatternNOS =              "patternNOS"
    aPatternScaleSubprofiles =  MObject();  anPatternScaleSubprofiles = "patternScaleSubprofiles"
    aRotateProfile =            MObject();  anRotateProfile =           "rotateProfile"
    aRPolygonInnerRadius =      MObject();  anRPolygonInnerRadius =     "rPolygonInnerRadius"
    aRPolygonSides =            MObject();  anRPolygonSides =           "rPolygonSides"
    aRPolygonType =             MObject();  anRPolygonType =            "rPolygonType"
    aScaleProfile =             MObject();  anScaleProfile =            "scaleProfile"
    aTwist =                    MObject();  anTwist =                   "twist"
    aWireProfileIndex =         MObject();  anWireProfileIndex =        "wireProfileIndex"

    # WIRE PROFILES
    rPolygonWireProfileIndex =  0;          rPolygonWireProfileName =   "RPolygon" 
    lineWireProfileIndex =      1;          lineWireProfileName =       "Line" 
    customWireProfileIndex =    2;          customWireProfileName =     "Custom"

    # VALUES
    defaultInterpolationDistance =          3.0
    defaultInterpolationRange =             0       # enum
    defaultInterpolationSteps =             20
    defaultNormalsReverse =                 False
    defaultNormalsSmoothing =               60.0
    defaultPatternCoverage =                1.0
    defaultPatternEnable =                  False
    defaultPatternLayout =                  0       # enum
    defaultPatternNOS =                     5
    defaultPatternScaleSubprofiles =        0.5
    defaultRotateProfile =                  0
    defaultRPolygonInnerRadius =            0.5
    defaultRPolygonSides =                  8
    defaultRPolygonType =                   0       # enum
    defaultScaleProfile =                   1.0
    defaultTwist =                          0.0
    defaultWireProfileIndex =               0       # enum

    minInterpolationDistance =              0.01
    minInterpolationSteps =                 1
    minNormalsSmoothing =                   0.0
    minPatternCoverage =                    0.0
    minPatternNOS =                         1
    minPatternScaleSubprofiles =            0.0
    minRotateProfile =                      -360.0
    minRPolygonInnerRadius =                0.0
    minRPolygonSides =                      3
    minScaleProfile =                       0.0

    maxNormalsSmoothing =                   180.0
    maxPatternCoverage =                    1.0
    maxPatternNOS =                         1000
    maxPatternScaleSubprofiles =            10000.0
    maxRotateProfile =                      360.0
    maxRPolygonInnerRadius =                1.0
    maxRPolygonSides =                      80
    maxScaleProfile =                       1000000.0

    #-------------------------------------------------------------------------#
    #   CONSTRUCTOR
    #-------------------------------------------------------------------------#
    def __init__(self, *args, **kwargs):
        # INITIALIZE
        super(WireMeshCreatorNode, self).__init__(*args, **kwargs)

        self.backupData =           WMCNBD()
        self.computeFlagMap = {
            "topology":             False,
            "wireProfile:":         False,
            "normals":              False
        }

        self.wireProfileDataMap = {
            WireMeshCreatorNode.rPolygonWireProfileIndex:   None,
            WireMeshCreatorNode.lineWireProfileIndex:       None,
            WireMeshCreatorNode.customWireProfileIndex:     None
        }

    #-------------------------------------------------------------------------#
    #   COMPUTE
    #-------------------------------------------------------------------------#
    def compute(self, plug, dataBlock):
        # COMPUTE FLAGS
        # reset
        self.computeFlagMap["topology"] =      False
        self.computeFlagMap["wireProfile"] =   False
        self.computeFlagMap["normals"] =       False
        # set
        self.computeFlagMap = self.backupData.compareData(dataBlock, self.computeFlagMap)

        # ATTRIBUTE : OUT MESH ARRAY
        if plug == WireMeshCreatorNode.aOutMeshArray:
            # CHECK
            pOutMeshArrayElementList = []
            if plug.isArray == True:
                for i in range(plug.numElements()):
                    pOutMeshArrayElementList.append(plug.elementByPhysicalIndex(i))
            else:
                pOutMeshArrayElementList.append(plug)
            
            # This function should return quickly (before any calculations are made) 
            # if there are missing relations between corresponding logical indices of
            # 'inCurveArray' and 'outMeshArray' plugs.
            # For example if you have 3 curves connected to this node, their initial
            # logical indices are: 0, 1, 2. 'inCurveArray[0]' is related to 'outMeshArray[0]',
            # 'inCurveArray[1]' is related to 'outMeshArray[1]', etc. If you delete second
            # connection between curve and this node ('inCurveArray[1]') there is
            # no point of calculating anything for 'outMeshArray[1]' plug.
            fnDependencyNode = MFnDependencyNode(self.thisMObject())
            pInCurveArray = fnDependencyNode.findPlug(WireMeshCreatorNode.aInCurveArray, True)

            for pOutMeshArrayElement in pOutMeshArrayElementList:
                pInCurveArrayElement = pInCurveArray.elementByLogicalIndex(pOutMeshArrayElement.logicalIndex())

                if pOutMeshArrayElement.isConnected and pInCurveArrayElement.isConnected:
                    self._computeOutMeshArrayElement(pOutMeshArrayElement, pInCurveArrayElement, dataBlock)

            # CLEAN
            dataBlock.setClean(plug)

    #-------------------------------------------------------------------------#
    #   _ COMPUTE OUT MESH ARRAY ELEMENT
    #-------------------------------------------------------------------------#
    def _computeOutMeshArrayElement(self, pOutMeshArrayElement, pInCurveArrayElement, dataBlock):
        #-------------------------------------------------------------------------#
        #   READ
        #-------------------------------------------------------------------------#
        voCurve =                   dataBlock.inputValue(pInCurveArrayElement).asNurbsCurveTransformed()

        interpolationDistance =     self.backupData.interpolationDistance
        interpolationRange =        self.backupData.interpolationRange
        interpolationSteps =        self.backupData.interpolationSteps
        normalsReverse =            self.backupData.normalsReverse
        normalsSmoothing =          self.backupData.normalsSmoothing
        rotateProfile =             self.backupData.rotateProfile
        scaleProfile =              self.backupData.scaleProfile
        twist =                     self.backupData.twist
        wireProfileIndex =          self.backupData.wireProfileIndex

        #-------------------------------------------------------------------------#
        #   PROCESS
        #-------------------------------------------------------------------------#
        # WIRE PROFILE
        self.activeWireProfileData = self._getWireProfileData(wireProfileIndex)

        # SETUP WIRE SECTION BUILD INFORMATION
        fnNURBSCurve =              MFnNurbsCurve(voCurve)
        curveLength =               fnNURBSCurve.length()
        wireSectionBuildInfoList =  []

        # start to end interpolation
        if interpolationRange == 0:
            for step in range(interpolationSteps + 1):
                param =                 fnNURBSCurve.findParamFromLength((curveLength / interpolationSteps) * step)
                tangent =               fnNURBSCurve.tangent(param).normalize()
                adjustOnEP =            False
                stepBackTangent =       MVector(0.0, 0.0, 0.0)
                wireSectionBuildInfo =  (param, tangent, adjustOnEP, stepBackTangent)
                wireSectionBuildInfoList.append(wireSectionBuildInfo)

        # ep to ep interpolation
        elif interpolationRange == 1:
            tangent =               fnNURBSCurve.tangent(0.0).normalize()
            adjustOnEP =            False
            stepBackTangent =       MVector(0.0, 0.0, 0.0)
            wireSectionBuildInfo =  (0.0, tangent, adjustOnEP, stepBackTangent)
            wireSectionBuildInfoList.append(wireSectionBuildInfo)
                
            lastKnot = 0.0
            for knot in fnNURBSCurve.knots():
                if knot != lastKnot:
                    startLength = fnNURBSCurve.findLengthFromParam(lastKnot) 
                    endLength = fnNURBSCurve.findLengthFromParam(knot)
                    lengthRange = endLength - startLength

                    for step in range(1, interpolationSteps + 1):
                        # There is possibility to omit getting params from length and
                        # get those straight up from knots, but it yields non-uniform 
                        # spacing between wire sections.
                        param = fnNURBSCurve.findParamFromLength(
                            startLength + (lengthRange / interpolationSteps) * step)
                        adjustOnEP = False
                        stepBackTangent = MVector(0.0, 0.0, 0.0)

                        if step == interpolationSteps:
                            adjustOnEP = True

                            accuracy = 10000.0
                            stepBackTangentParam = fnNURBSCurve.findParamFromLength(
                                startLength + (lengthRange / accuracy) * (accuracy - 1.0))
                            stepBackTangent = fnNURBSCurve.tangent(stepBackTangentParam).normalize()

                        tangent =               fnNURBSCurve.tangent(param).normalize()
                        wireSectionBuildInfo =  (param, tangent, adjustOnEP, stepBackTangent)
                        wireSectionBuildInfoList.append(wireSectionBuildInfo)

                    lastKnot = knot

        # distance interpolation
        elif interpolationRange == 2:
            curveDistance =         0.0
            distanceSafeThreshold = interpolationDistance * 0.3
            while (curveDistance < curveLength - distanceSafeThreshold):
                param =                 fnNURBSCurve.findParamFromLength(curveDistance)
                tangent =               fnNURBSCurve.tangent(param).normalize()
                adjustOnEP =            False
                stepBackTangent =       MVector(0.0, 0.0, 0.0)
                wireSectionBuildInfo =  (param, tangent, adjustOnEP, stepBackTangent)
                wireSectionBuildInfoList.append(wireSectionBuildInfo)

                curveDistance += interpolationDistance

            param =                 fnNURBSCurve.findParamFromLength(curveLength)
            tangent =               fnNURBSCurve.tangent(param).normalize()
            adjustOnEP =            False
            stepBackTangent =       MVector(0.0, 0.0, 0.0)
            wireSectionBuildInfo =  (param, tangent, adjustOnEP, stepBackTangent)
            wireSectionBuildInfoList.append(wireSectionBuildInfo)

        # CREATE WIRE SECTIONS
        wireSectionList = []

        for (param, tangent, adjustOnEP, stepBackTangent) in wireSectionBuildInfoList:
            wireSection = WireSection(self.activeWireProfileData)

            # translate
            point = fnNURBSCurve.getPointAtParam(param)
            wireSection.setTranslation(point)

            # rotate
            if (len(wireSectionList) == 0):
                # First wire section is rotated in a way that omits rotation around
                # local z axis. Comparing this to FPS camera movement we would 
                # say that there is no roll transformation, only pitch and yawn.
                xRotation = 0.0
                tangentProjection = MVector(tangent.x, 0.0, tangent.z)
                if (tangentProjection != tangent):
                    if (tangent.x == 0 and tangent.z == 0):
                        xRotation = math.radians(90.0)
                    else:
                        xRotation = math.acos(
                            mathUtils.dot(tangent, tangentProjection)
                            / (tangent.length() * tangentProjection.length())
                        )

                    if (tangent.y > 0.0):
                        xRotation = -xRotation

                yRotation = 0.0
                if (tangentProjection != MVector(0.0, 0.0, 0.0)):
                    yRotation = math.acos(
                        mathUtils.dot(tangentProjection, MVector(0.0, 0.0, 1.0))
                        / tangentProjection.length()
                    )
                    if (tangentProjection.x < 0.0):
                        yRotation = -yRotation 

                wireSection.rotate(
                    MEulerRotation(xRotation, yRotation, 0.0),
                    WireSection.RotationType.ALIGN_WITH_TANGENT
                )

            else:
                previousWireSection = wireSectionList[-1]
                alignWithTangentRotation \
                    = previousWireSection.getRotationOfType(WireSection.RotationType.ALIGN_WITH_TANGENT) \
                    * previousWireSection.getRotationOfType(WireSection.RotationType.ADJUST_ON_EP) \
                    * MQuaternion(previousWireSection.getLocalZAxis(), tangent)

                wireSection.rotate(
                    alignWithTangentRotation,
                    WireSection.RotationType.ALIGN_WITH_TANGENT
                )

                if adjustOnEP == True and fnNURBSCurve.degree == 1:
                    wireSection.rotate(
                        MQuaternion(wireSection.getLocalZAxis(), stepBackTangent, 0.5),
                        WireSection.RotationType.ADJUST_ON_EP
                    )

            if (rotateProfile != 0.0):
                wireSection.rotate(
                    MQuaternion(math.radians(rotateProfile), wireSection.getLocalZAxis()),
                    WireSection.RotationType.CUSTOM_PROFILE_ROTATION
                )

            if (twist != 0.0):
                curveLengthToPoint = fnNURBSCurve.findLengthFromParam(param)

                twistRotationAngle = math.radians(twist * (curveLengthToPoint / curveLength))
                twistRotation = MQuaternion(twistRotationAngle, wireSection.getLocalZAxis())

                wireSection.rotate(
                    twistRotation,
                    WireSection.RotationType.TWIST
                )

            # scale
            wireSection.setScale(scaleProfile, scaleProfile, 1.0)

            if adjustOnEP == True and fnNURBSCurve.degree == 1:
                transformationMatrix =      MTransformationMatrix()
                stepBackTangentOpposite =   stepBackTangent * -1
                    
                transformationMatrix.setRotation(MQuaternion(
                    tangent, stepBackTangentOpposite, 0.5))

                scaleVector =   tangent * transformationMatrix.asMatrix()
                scaleValue =    1 / math.sin(scaleVector.angle(stepBackTangentOpposite))

                wireSection.scaleAlongVector(scaleValue, scaleVector)

            # add
            wireSectionList.append(wireSection)
                
        # GENERATE MESH DATA
        vertexList =            []
        polygonOffsetList =     []
        vertexSequenceList =    []
        numSubprofiles =        self.activeWireProfileData.getNumSubprofiles()

        for i in range(numSubprofiles):
            subprofileSize = self.activeWireProfileData.getSubprofileSize(i)

            # vertex list
            for wireSection in wireSectionList:
                if (normalsReverse == True):    # reverse normals / change drawing order
                    vertexList.extend(list(reversed(wireSection.getSubprofilePoints(i))))
                else:
                    vertexList.extend(wireSection.getSubprofilePoints(i))

            # polygon offset list
            numQuads = 0
            if self.activeWireProfileData.isSubprofileClosed(i) == True:
                numQuads = subprofileSize * (len(wireSectionList) - 1)
            else:
                numQuads = (subprofileSize - 1) * (len(wireSectionList) - 1)

            polygonOffsetList.extend([4] * numQuads)       # [4, 4, 4, ...]

            # vertex sequence list
            meshJump = i * subprofileSize * len(wireSectionList)
            for j in range(len(wireSectionList)-1):
                wireSectionJump = j * subprofileSize
                for k in range(subprofileSize-1):
                    vertexSequenceList.extend([
                        meshJump + wireSectionJump + k,
                        meshJump + wireSectionJump + k + 1,
                        meshJump + wireSectionJump + subprofileSize + 1 + k,
                        meshJump + wireSectionJump + subprofileSize + k
                    ])
                if self.activeWireProfileData.isSubprofileClosed(i) == True:
                    vertexSequenceList.extend([
                        meshJump + wireSectionJump + subprofileSize - 1,
                        meshJump + wireSectionJump,
                        meshJump + wireSectionJump + subprofileSize,
                        meshJump + wireSectionJump + (2 * subprofileSize) - 1
                    ])

        # CREATE MESH
        fnMesh =        MFnMesh()
        fnMeshData =    MFnMeshData()
        oMeshData =     fnMeshData.create()
        oMesh =         fnMesh.create(vertexList, polygonOffsetList, vertexSequenceList,
                            parent = oMeshData)

        # SET NORMALS SMOOTHING
        #if (self.computeFlagMap["normals"] == True):   # << ADD LATER WHEN self.computeFlagMap["topology"]
                                                            # is implemented for topology creation
        itMeshEdge = MItMeshEdge(oMesh)

        if (normalsSmoothing == 0.0):       # hard edge
            while (itMeshEdge.isDone() == False):
                fnMesh.setEdgeSmoothing(itMeshEdge.index(), False)
                itMeshEdge.next()

        elif (normalsSmoothing == 180.0):   # soft edge
            while (itMeshEdge.isDone() == False):
                fnMesh.setEdgeSmoothing(itMeshEdge.index(), True)
                itMeshEdge.next()

        else:
            while (itMeshEdge.isDone() == False):
                if (itMeshEdge.numConnectedFaces() == 2):
                    faceIDList =    itMeshEdge.getConnectedFaces()
                    faceNormal1 =   fnMesh.getPolygonNormal(faceIDList[0])
                    faceNormal2 =   fnMesh.getPolygonNormal(faceIDList[1])
                    angleRad =      faceNormal1.angle(faceNormal2)

                    if (angleRad <= math.radians(normalsSmoothing)):
                        fnMesh.setEdgeSmoothing(itMeshEdge.index(), True)
                    else:
                        fnMesh.setEdgeSmoothing(itMeshEdge.index(), False)

                itMeshEdge.next()

        fnMesh.cleanupEdgeSmoothing()

        #-------------------------------------------------------------------------#
        #   OUTPUT
        #-------------------------------------------------------------------------#
        dataBlock.outputValue(pOutMeshArrayElement).setMObject(oMeshData)
        dataBlock.setClean(pOutMeshArrayElement)

    #-------------------------------------------------------------------------#
    #   _ GET WIRE PROFILE DATA
    #-------------------------------------------------------------------------#
    def _getWireProfileData(self, wireProfileIndex):
        if self.computeFlagMap["wireProfile"] == True: # create if needed
            if wireProfileIndex == WireMeshCreatorNode.rPolygonWireProfileIndex:
                self.wireProfileDataMap[wireProfileIndex] = self._createRPolygonWireProfileData()

            elif wireProfileIndex == WireMeshCreatorNode.lineWireProfileIndex:
                self.wireProfileDataMap[wireProfileIndex] = self._createLineWireProfileData()

        return self.wireProfileDataMap[wireProfileIndex]

    #-------------------------------------------------------------------------#
    #   _ CREATE REGULAR POLYGON WIRE PROFILE DATA
    #-------------------------------------------------------------------------#
    def _createRPolygonWireProfileData(self):
        rPolygonSubprofilePointList = []

        if self.backupData.rPolygonType == 0:   # convex
            rPolygonSubprofilePointList = mathUtils.createPolygonPointList(self.backupData.rPolygonSides)
        else:                                   # star
            rPolygonSubprofilePointList = mathUtils.createPolygonPointList(self.backupData.rPolygonSides * 2)
            for i in range(len(rPolygonSubprofilePointList)):
                if i % 2 == 1:
                    rPolygonSubprofilePointList[i] *= self.backupData.rPolygonInnerRadius

        rPolygonSubprofile = WireSubprofile(rPolygonSubprofilePointList, True)

        if self.backupData.patternEnable == True:
            rPolygonWireProfileData = self._createPatternWireProfileData(rPolygonSubprofile)
        else:
            rPolygonWireProfileData = WireProfileData([rPolygonSubprofile])

        return rPolygonWireProfileData

    #-------------------------------------------------------------------------#
    #   _ CREATE LINE WIRE PROFILE DATA
    #-------------------------------------------------------------------------#
    def _createLineWireProfileData(self):
        lineSubprofilePointList = [
            MPoint( 1.0, 0.0),
            MPoint(-1.0, 0.0)
        ]
        lineSubprofile = WireSubprofile(lineSubprofilePointList, False)

        if self.backupData.patternEnable == True:
            lineWireProfileData = self._createPatternWireProfileData(lineSubprofile)
        else:
            lineWireProfileData = WireProfileData([lineSubprofile])

        return lineWireProfileData

    #-------------------------------------------------------------------------#
    #   _ CREATE PATTERN WIRE PROFILE DATA
    #-------------------------------------------------------------------------#
    def _createPatternWireProfileData(self, wireSubprofile):
        # PRE-PLACEMENT TRANSFORMATIONS
        prePlacementPointList =     []
        ppTransformationMatrix =    MTransformationMatrix()
        scaleValue =                self.backupData.patternScaleSubprofiles

        ppTransformationMatrix.setScale((scaleValue, scaleValue, 1.0), MSpace.kTransform)

        for point in wireSubprofile.getPointList():
            prePlacementPointList.append(point * ppTransformationMatrix.asMatrix())
        
        # PLACEMENT TRANSFORMATIONS
        patternSubprofileList = []

        # circle layout
        if self.backupData.patternLayout == 0:
            eulerRotation =         MEulerRotation()
            radianSteps =           math.radians(360.0 / self.backupData.patternNOS) * self.backupData.patternCoverage
            pTransformationMatrix = MTransformationMatrix()
            pTransformationMatrix.setTranslation(MVector(0.0, 1.0, 0.0), MSpace.kTransform)
            pTransformationMatrix.setRotatePivot(MPoint(0.0, -1.0, 0.0), MSpace.kTransform, True)

            for i in range(self.backupData.patternNOS):
                eulerRotation.z = radianSteps * i
                pTransformationMatrix.setRotation(eulerRotation)

                patternSubprofilePointList = []
                for point in prePlacementPointList:
                    patternSubprofilePointList.append(point * pTransformationMatrix.asMatrix())

                patternSubprofileList.append(WireSubprofile(patternSubprofilePointList, wireSubprofile.isClosed()))

        # line layout
        elif self.backupData.patternLayout == 1:
            for i in range(self.backupData.patternNOS):
                translateVector = MVector(0.0, 0.0, 0.0)
                if self.backupData.patternNOS > 1:
                    translateVector.x = i * self.backupData.patternCoverage / (self.backupData.patternNOS - 1) # 0 to 1 range
                translateVector.x *= 2.0 # 0 to 2 range
                translateVector.x -= 1.0 # -1 to 1 range

                patternSubprofilePointList = []
                for point in prePlacementPointList:
                    patternSubprofilePointList.append(point + translateVector)

                patternSubprofileList.append(WireSubprofile(patternSubprofilePointList, wireSubprofile.isClosed()))

        return WireProfileData(patternSubprofileList)

    #-------------------------------------------------------------------------#
    #   NODE INITIALIZER
    #-------------------------------------------------------------------------#
    @staticmethod
    def nodeInitializer():
        #-------------------------------------------------------------------------#
        #   ATTRIBUTES
        #-------------------------------------------------------------------------#
        fnEnumAttribute =       MFnEnumAttribute()
        fnNumericAttribute =    MFnNumericAttribute()
        fnTypedAttribute =      MFnTypedAttribute()

        # SETUP
        # wire profile shapes
        WireMeshCreatorNode.aWireProfileIndex = fnEnumAttribute.create(
            WireMeshCreatorNode.anWireProfileIndex, 
            WireMeshCreatorNode.anWireProfileIndex
        )
        fnEnumAttribute.addField(
            WireMeshCreatorNode.rPolygonWireProfileName,
            WireMeshCreatorNode.rPolygonWireProfileIndex
        )
        fnEnumAttribute.addField(
            WireMeshCreatorNode.lineWireProfileName,
            WireMeshCreatorNode.lineWireProfileIndex
        )
        fnEnumAttribute.addField(
            WireMeshCreatorNode.customWireProfileName,
            WireMeshCreatorNode.customWireProfileIndex
        )
        fnEnumAttribute.default = WireMeshCreatorNode.defaultWireProfileIndex
        fnEnumAttribute.connectable = False

        # custom wire profile data
        WireMeshCreatorNode.aCustomWireProfileData = fnTypedAttribute.create(
            WireMeshCreatorNode.anCustomWireProfileData, 
            WireMeshCreatorNode.anCustomWireProfileData, 
            WireProfileData.dataID
        )
        fnTypedAttribute.readable = False
        fnTypedAttribute.storable = False

        # rpolygon wire profile type
        WireMeshCreatorNode.aRPolygonType = fnEnumAttribute.create(
            WireMeshCreatorNode.anRPolygonType, 
            WireMeshCreatorNode.anRPolygonType
        )
        fnEnumAttribute.addField("Convex", 0)
        fnEnumAttribute.addField("Star", 1)
        fnEnumAttribute.default = WireMeshCreatorNode.defaultRPolygonType
        fnEnumAttribute.connectable = False

        # rpolygon wire profile sides
        WireMeshCreatorNode.aRPolygonSides = fnNumericAttribute.create(
            WireMeshCreatorNode.anRPolygonSides, 
            WireMeshCreatorNode.anRPolygonSides, 
            MFnNumericData.kInt
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minRPolygonSides)
        fnNumericAttribute.setMax(WireMeshCreatorNode.maxRPolygonSides)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultRPolygonSides

        # rpolygon wire profile inner radius
        WireMeshCreatorNode.aRPolygonInnerRadius = fnNumericAttribute.create(
            WireMeshCreatorNode.anRPolygonInnerRadius, 
            WireMeshCreatorNode.anRPolygonInnerRadius, 
            MFnNumericData.kFloat
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minRPolygonInnerRadius)
        fnNumericAttribute.setMax(WireMeshCreatorNode.maxRPolygonInnerRadius)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultRPolygonInnerRadius

        # pattern enable
        WireMeshCreatorNode.aPatternEnable = fnNumericAttribute.create(
            WireMeshCreatorNode.anPatternEnable, 
            WireMeshCreatorNode.anPatternEnable, 
            MFnNumericData.kBoolean
        )
        fnNumericAttribute.default = WireMeshCreatorNode.defaultPatternEnable
        fnNumericAttribute.connectable = False

        # pattern layout
        WireMeshCreatorNode.aPatternLayout = fnEnumAttribute.create(
            WireMeshCreatorNode.anPatternLayout, 
            WireMeshCreatorNode.anPatternLayout
        )
        fnEnumAttribute.addField("Circle", 0)
        fnEnumAttribute.addField("Line", 1)
        fnEnumAttribute.default = WireMeshCreatorNode.defaultPatternLayout
        fnEnumAttribute.connectable = False

        # pattern nos (number of subprofiles)
        WireMeshCreatorNode.aPatternNOS = fnNumericAttribute.create(
            WireMeshCreatorNode.anPatternNOS, 
            WireMeshCreatorNode.anPatternNOS, 
            MFnNumericData.kInt
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minPatternNOS)
        fnNumericAttribute.setMax(WireMeshCreatorNode.maxPatternNOS)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultPatternNOS

        # pattern scale subprofiles
        WireMeshCreatorNode.aPatternScaleSubprofiles = fnNumericAttribute.create(
            WireMeshCreatorNode.anPatternScaleSubprofiles, 
            WireMeshCreatorNode.anPatternScaleSubprofiles, 
            MFnNumericData.kFloat
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minPatternScaleSubprofiles)
        fnNumericAttribute.setMax(WireMeshCreatorNode.maxPatternScaleSubprofiles)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultPatternScaleSubprofiles

        # pattern coverage
        WireMeshCreatorNode.aPatternCoverage = fnNumericAttribute.create(
            WireMeshCreatorNode.anPatternCoverage, 
            WireMeshCreatorNode.anPatternCoverage, 
            MFnNumericData.kFloat
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minPatternCoverage)
        fnNumericAttribute.setMax(WireMeshCreatorNode.maxPatternCoverage)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultPatternCoverage

        # interpolation range
        WireMeshCreatorNode.aInterpolationRange = fnEnumAttribute.create(
            WireMeshCreatorNode.anInterpolationRange, 
            WireMeshCreatorNode.anInterpolationRange
        )
        fnEnumAttribute.addField("Start to End", 0)
        fnEnumAttribute.addField("EP to EP", 1)
        fnEnumAttribute.addField("Distance", 2)
        fnEnumAttribute.default = WireMeshCreatorNode.defaultInterpolationRange
        fnEnumAttribute.connectable = False

        # interpolation steps
        WireMeshCreatorNode.aInterpolationSteps = fnNumericAttribute.create(
            WireMeshCreatorNode.anInterpolationSteps, 
            WireMeshCreatorNode.anInterpolationSteps, 
            MFnNumericData.kInt
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minInterpolationSteps)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultInterpolationSteps
        fnNumericAttribute.keyable = True

        # interpolation distance
        WireMeshCreatorNode.aInterpolationDistance = fnNumericAttribute.create(
            WireMeshCreatorNode.anInterpolationDistance, 
            WireMeshCreatorNode.anInterpolationDistance, 
            MFnNumericData.kFloat
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minInterpolationDistance)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultInterpolationDistance
        fnNumericAttribute.keyable = True

        # scale profile
        WireMeshCreatorNode.aScaleProfile = fnNumericAttribute.create(
            WireMeshCreatorNode.anScaleProfile, 
            WireMeshCreatorNode.anScaleProfile, 
            MFnNumericData.kFloat
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minScaleProfile)
        fnNumericAttribute.setMax(WireMeshCreatorNode.maxScaleProfile)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultScaleProfile
        fnNumericAttribute.keyable = True

        # rotate profile
        WireMeshCreatorNode.aRotateProfile = fnNumericAttribute.create(
            WireMeshCreatorNode.anRotateProfile, 
            WireMeshCreatorNode.anRotateProfile, 
            MFnNumericData.kFloat
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minRotateProfile)
        fnNumericAttribute.setMax(WireMeshCreatorNode.maxRotateProfile)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultRotateProfile
        fnNumericAttribute.keyable = True

        # twist
        WireMeshCreatorNode.aTwist = fnNumericAttribute.create(
            WireMeshCreatorNode.anTwist, 
            WireMeshCreatorNode.anTwist, 
            MFnNumericData.kFloat
        )
        fnNumericAttribute.default = WireMeshCreatorNode.defaultTwist
        fnNumericAttribute.keyable = True

        # normals reverse
        WireMeshCreatorNode.aNormalsReverse = fnNumericAttribute.create(
            WireMeshCreatorNode.anNormalsReverse, 
            WireMeshCreatorNode.anNormalsReverse, 
            MFnNumericData.kBoolean
        )
        fnNumericAttribute.default = WireMeshCreatorNode.defaultNormalsReverse

        # normals smoothing
        WireMeshCreatorNode.aNormalsSmoothing = fnNumericAttribute.create(
            WireMeshCreatorNode.anNormalsSmoothing, 
            WireMeshCreatorNode.anNormalsSmoothing, 
            MFnNumericData.kFloat
        )
        fnNumericAttribute.setMin(WireMeshCreatorNode.minNormalsSmoothing)
        fnNumericAttribute.setMax(WireMeshCreatorNode.maxNormalsSmoothing)
        fnNumericAttribute.default = WireMeshCreatorNode.defaultNormalsSmoothing

        # in curve array
        WireMeshCreatorNode.aInCurveArray = fnTypedAttribute.create(
            WireMeshCreatorNode.anInCurveArray,
            WireMeshCreatorNode.anInCurveArray, 
            MFnData.kNurbsCurve
        )
        fnTypedAttribute.readable =             False
        fnTypedAttribute.storable =             False
        fnTypedAttribute.cached =               False
        fnTypedAttribute.array =                True
        fnTypedAttribute.indexMatters =         False

        # out mesh array
        WireMeshCreatorNode.aOutMeshArray = fnTypedAttribute.create(
            WireMeshCreatorNode.anOutMeshArray, 
            WireMeshCreatorNode.anOutMeshArray, 
            MFnData.kMesh
        )
        fnTypedAttribute.writable =             False
        fnTypedAttribute.array =                True
        fnTypedAttribute.usesArrayDataBuilder = True

        # ADD
        MPxNode.addAttribute(WireMeshCreatorNode.aWireProfileIndex)
        MPxNode.addAttribute(WireMeshCreatorNode.aCustomWireProfileData)
        MPxNode.addAttribute(WireMeshCreatorNode.aRPolygonType)
        MPxNode.addAttribute(WireMeshCreatorNode.aRPolygonSides)
        MPxNode.addAttribute(WireMeshCreatorNode.aRPolygonInnerRadius)
        MPxNode.addAttribute(WireMeshCreatorNode.aPatternEnable)
        MPxNode.addAttribute(WireMeshCreatorNode.aPatternLayout)
        MPxNode.addAttribute(WireMeshCreatorNode.aPatternNOS)
        MPxNode.addAttribute(WireMeshCreatorNode.aPatternScaleSubprofiles)
        MPxNode.addAttribute(WireMeshCreatorNode.aPatternCoverage)
        MPxNode.addAttribute(WireMeshCreatorNode.aInterpolationRange)
        MPxNode.addAttribute(WireMeshCreatorNode.aInterpolationSteps)
        MPxNode.addAttribute(WireMeshCreatorNode.aInterpolationDistance)
        MPxNode.addAttribute(WireMeshCreatorNode.aScaleProfile)
        MPxNode.addAttribute(WireMeshCreatorNode.aRotateProfile)
        MPxNode.addAttribute(WireMeshCreatorNode.aNormalsReverse)
        MPxNode.addAttribute(WireMeshCreatorNode.aNormalsSmoothing)
        MPxNode.addAttribute(WireMeshCreatorNode.aTwist)
        MPxNode.addAttribute(WireMeshCreatorNode.aInCurveArray)
        MPxNode.addAttribute(WireMeshCreatorNode.aOutMeshArray)

        # CONNECT
        # out mesh array
        MPxNode.attributeAffects(WireMeshCreatorNode.aWireProfileIndex, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aCustomWireProfileData, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aRPolygonType, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aRPolygonSides, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aRPolygonInnerRadius, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aPatternEnable, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aPatternLayout, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aPatternNOS, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aPatternScaleSubprofiles, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aPatternCoverage, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aInterpolationRange, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aInterpolationSteps, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aInterpolationDistance, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aScaleProfile, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aRotateProfile, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aNormalsReverse, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aNormalsSmoothing, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aTwist, WireMeshCreatorNode.aOutMeshArray)
        MPxNode.attributeAffects(WireMeshCreatorNode.aInCurveArray, WireMeshCreatorNode.aOutMeshArray)

    #-------------------------------------------------------------------------#
    #   NODE CREATOR
    #-------------------------------------------------------------------------#
    @staticmethod
    def nodeCreator():
        return WireMeshCreatorNode()
