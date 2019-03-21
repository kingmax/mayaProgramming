#-------------------------------------------------------------------------#
#   CREATED:
#       22 IX 2017
#   INFO:
#       A few words about this file... 
#
#       1.  Name of the class is super important. It should follow
#           AE<nodeName>Template convention, otherwise PyMEL will not
#           load this custom AE template into Maya. Documentation also
#           mentions about a second method: 
#               
#               "set its _nodeType class attribute to the name of the 
#               desired node type"
#               Source: http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.uitypes/pymel.core.uitypes.AETemplate.html
#               
#           Unfortunately I didn't have much success with that.
#           
#       2.  I have seen some plugins adding "callbacks" command on
#           plugin loading code. Example:
#           
#               cmds.callbacks(
#                   addCallback =   AEwireMeshCreatorTemplate.aeTemplateCreator,
#                   hook =          "AETemplateCustomContent",
#                   owner =         WireMeshCreatorNode.nodeName
#               )
#
#           Well, I'm not Maya expert but after some testing this does not
#           have effect on anything. If you checked "Auto load" checkbox
#           for your plugin in Plugin Manager then this callback will be
#           invoked when you open Maya but even without this custom AE
#           template will work because this module will be loaded eventually. 
#           But again I'm not Maya expert so I may missing something here...
#
#       3.  *Connect functions are invoked every time you have Attribute Editor
#           raised and either create a new node or select a node.
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
#   IMPORTS
#-------------------------------------------------------------------------#
from functools import partial

import maya.cmds as cmds
import pymel.core as pm

from wiresrc.wireMeshCreatorNode import WireMeshCreatorNode

#-------------------------------------------------------------------------#
#   CLASS DEFINITIONS
#   ATTRIBUTE EDITOR WIRE MESH CREATOR TEMPLATE
#-------------------------------------------------------------------------#
class AEwireMeshCreatorTemplate(pm.uitypes.AETemplate):
    #-------------------------------------------------------------------------#
    #   STATIC CLASS MEMBERS
    #-------------------------------------------------------------------------#
    imageBackgroundColorActive =    (82.0/255.0, 82.0/255.0, 82.0/255.0) 
    textBackgroundColorActive =     (235.0/255.0, 154.0/255.0, 94.0/255.0)
    textBackgroundColorInactive =   (56.0/255.0, 56.0/255.0, 56.0/255.0)

    #-------------------------------------------------------------------------#
    #   CONSTRUCTOR
    #   (str)
    #-------------------------------------------------------------------------#
    def __init__(self, nodeName):
        super(AEwireMeshCreatorTemplate, self).__init__(nodeName)

        self.activeNodeName =                       nodeName
        self.activeWireProfilesIndex =              WireMeshCreatorNode.defaultWireProfileIndex

        self.iterpolationDistanceControlID =        None 
        self.iterpolationRangeControlID =           None
        self.iterpolationStepsControlID =           None
        self.normalsSmoothingControlID =            None
        self.patternCoverageControlID =             None
        self.patternLayoutControlID =               None
        self.patternNumberOfSubprofilesControlID =  None
        self.patternScaleSubprofilesControlID =     None
        self.rotateProfileControlID =               None
        self.rPolygonInnerRadiusControlID =         None
        self.rPolygonSidesControlID =               None
        self.rPolygonTypeControlID =                None
        self.scaleProfileControlID =                None
        self.twistControlID =                       None

        # SETUP
        self._setupUI()

    #-------------------------------------------------------------------------#
    #   _ SETUP UI
    #-------------------------------------------------------------------------#
    def _setupUI(self):
        # CLEAR ATTRIBUTE EDITOR CONTENT
        for attribute in pm.listAttr(self.nodeName):
            self.suppress(attribute)

        # MAIN LAYOUT
        self.beginScrollLayout()

        # SET NODE NAME
        self.callCustom(
            self.setNodeName, 
            self.setNodeNameConnect,
            "setNodeName" # fake attribute name
        )

        # NODE HEADER
        self.callCustom(
            self.nodeHeaderLayout, 
            self.nodeHeaderLayoutConnect,
            "nodeHeaderLayout" # fake attribute name
        )

        # WIRE PROFILES
        self.beginLayout("Wire Profiles", collapse=False)
        self.callCustom(
            self.wireProfilesLayout, 
            self.wireProfilesLayoutConnect,
            WireMeshCreatorNode.anWireProfileIndex
        )
        self.beginLayout("RPolygon", collapse=False)
        self.callCustom(
           self.rPolygonTypeControl,
           self.rPolygonTypeControlConnect,
           WireMeshCreatorNode.anRPolygonType
        )
        self.callCustom(
           self.rPolygonSidesControl,
           self.rPolygonSidesControlConnect,
           WireMeshCreatorNode.anRPolygonSides
        )
        self.callCustom(
           self.rPolygonInnerRadiusControl,
           self.rPolygonInnerRadiusControlConnect,
           WireMeshCreatorNode.anRPolygonInnerRadius
        )
        self.endLayout()
        self.beginLayout("Pattern", collapse=True)
        self.addControl(
            WireMeshCreatorNode.anPatternEnable,
            label = "Pattern",
            changeCommand = self._patternEnableControlDimming
        )
        self.callCustom(
           self.patternLayoutControl,
           self.patternLayoutControlConnect,
           WireMeshCreatorNode.anPatternLayout
        )
        self.callCustom(
           self.patternNumberOfSubprofilesControl,
           self.patternNumberOfSubprofilesControlConnect,
           WireMeshCreatorNode.anPatternNOS
        )
        self.callCustom(
           self.patternScaleSubprofilesControl,
           self.patternScaleSubprofilesControlConnect,
           WireMeshCreatorNode.anPatternScaleSubprofiles
        )
        self.callCustom(
           self.patternCoverageControl,
           self.patternCoverageControlConnect,
           WireMeshCreatorNode.anPatternCoverage
        )
        self.endLayout()
        self.endLayout()

        # INTERPOLATION
        self.beginLayout("Interpolation", collapse=False)
        self.addControl(
            WireMeshCreatorNode.anInterpolationRange,
            label = "Range",
            changeCommand = self._interpolationRangeControlDimming
        )
        self.callCustom(
            self.interpolationStepsControl, 
            self.interpolationStepsControlConnect,
            WireMeshCreatorNode.anInterpolationSteps
        )
        self.callCustom(
            self.interpolationDistanceControl, 
            self.interpolationDistanceControlConnect,
            WireMeshCreatorNode.anInterpolationDistance
        )
        self.endLayout()

        # TRANSFORMATIONS
        self.beginLayout("Transformations", collapse=False)
        self.callCustom(
            self.scaleProfileControl, 
            self.scaleProfileControlConnect,
            WireMeshCreatorNode.anScaleProfile
        )
        self.callCustom(
            self.rotateProfileControl, 
            self.rotateProfileControlConnect,
            WireMeshCreatorNode.anRotateProfile
        )
        self.callCustom(
            self.twistControl, 
            self.twistControlConnect,
            WireMeshCreatorNode.anTwist
        )
        self.endLayout()

        # NORMALS
        self.beginLayout("Normals", collapse=True)
        self.addControl(
            WireMeshCreatorNode.anNormalsReverse,
            label = "Reverse"
        )
        self.callCustom(
            self.normalsSmoothingControl, 
            self.normalsSmoothingControlConnect,
            WireMeshCreatorNode.anNormalsSmoothing
        )
        self.endLayout()

        # STANDARD MAYA CONSTROLS
        pm.mel.eval("AEdependNodeTemplate " + self.nodeName)    # MAYA_LOCATION/scripts/AETemplates
        self.addExtraControls()

        self.endScrollLayout()

    #-------------------------------------------------------------------------#
    #   SET NODE NAME
    #-------------------------------------------------------------------------#
    def setNodeName(self, fakeFullAttributeName):
        """
        Sole purpose of this and next function is to update active (selected) 
        node name since it seems like self.nodeName is not updated and it 
        cannot be set explicitly via: self.node = variable (Maya complains).

        self.activeNodeName is used mostly to get and set appropriate attribute
        values.
        """

        self.setNodeNameConnect(fakeFullAttributeName)

    #-------------------------------------------------------------------------#
    #   SET NODE NAME CONNECT
    #-------------------------------------------------------------------------#
    def setNodeNameConnect(self, fakeFullAttributeName):
        self.activeNodeName = fakeFullAttributeName.split(".")[0]

    #-------------------------------------------------------------------------#
    #   NODE HEADER LAYOUT
    #-------------------------------------------------------------------------#
    def nodeHeaderLayout(self, fakeFullAttributeName):
        cmds.columnLayout(
            height =            36,
            adjustableColumn =  True,
            rowSpacing =        0
        )
        cmds.rowLayout(
            height =            30,
            numberOfColumns =   2,
            columnWidth =       [(1, 30), (2, 250)],
            columnAttach =      [(1, "both", 5), (2, "both", 0)],
            columnAlign =       [(1, "left"), (2, "left")],
            backgroundColor =   (0.286, 0.286, 0.286)
        )
        cmds.image(
            width =             20,    
            height =            20,
            image =             "ae_wireMeshCreator.png"
        )
        cmds.text(
            label =             "Wire Mesh Creator",
            enableBackground =  False,
            noBackground =      True

        )

        self.nodeHeaderLayoutConnect(fakeFullAttributeName)

    #-------------------------------------------------------------------------#
    #   NODE HEADER LAYOUT CONNECT
    #-------------------------------------------------------------------------#
    def nodeHeaderLayoutConnect(self, fakeFullAttributeName):
        pass
        
    #-------------------------------------------------------------------------#
    #   WIRE PROFILES LAYOUT
    #-------------------------------------------------------------------------#
    def wireProfilesLayout(self, fakeFullAttributeName):
        imageSize =             58
        textRowHeight =         10

        self.wireProfilesControlsMap = {}

        # BUTTONS
        flowLayoutID = cmds.flowLayout(height=75, wrap=True)

        # rpolygon
        cmds.rowColumnLayout(
            numberOfRows =      2,
            rowHeight =         [(1, imageSize), (2, textRowHeight)]
        )
        buttonID = cmds.symbolButton(
            annotation =        "",
            width =             imageSize,
            height =            imageSize,
            image =             "ae_rPolygonWireProfile.png"
        )
        textID = cmds.text(
            label =             WireMeshCreatorNode.rPolygonWireProfileName,
            font =              "tinyBoldLabelFont",
            backgroundColor =   AEwireMeshCreatorTemplate.textBackgroundColorInactive
        )
        self.wireProfilesControlsMap[WireMeshCreatorNode.rPolygonWireProfileIndex] = (buttonID, textID)

        # line
        cmds.setParent(flowLayoutID)
        cmds.rowColumnLayout(
            numberOfRows =      2,
            rowHeight =         [(1, imageSize), (2, textRowHeight)]
        )
        buttonID = cmds.symbolButton(
            annotation =        "",
            width =             imageSize,
            height =            imageSize,
            image =             "ae_lineWireProfile.png"
        )
        textID = cmds.text(
            label =             WireMeshCreatorNode.lineWireProfileName,
            font =              "tinyBoldLabelFont",
            backgroundColor =   AEwireMeshCreatorTemplate.textBackgroundColorInactive
        )
        self.wireProfilesControlsMap[WireMeshCreatorNode.lineWireProfileIndex] = (buttonID, textID)

        self.wireProfilesLayoutConnect(fakeFullAttributeName)

    #-------------------------------------------------------------------------#
    #   WIRE PROFILES LAYOUT CONNECT
    #-------------------------------------------------------------------------#
    def wireProfilesLayoutConnect(self, fakeFullAttributeName):
        # CONNECT COMMAND WITH BUTTONS
        for (key, value) in self.wireProfilesControlsMap.items():
            cmds.symbolButton(
                value[0], 
                edit =          True,
                command =       partial(self._selectWireProfiles, fakeFullAttributeName, key)
            )

        # HIGHLIGHT ACTIVE WIRE PROFILE SHAPE
        self.activeWireProfilesIndex = cmds.getAttr(fakeFullAttributeName)
        self._resetWireProfilesControls()
        self._highlightWireProfilesControls(self.activeWireProfilesIndex)

    #-------------------------------------------------------------------------#
    #   REGULAR POLYGON TYPE CONTROL
    #-------------------------------------------------------------------------#
    def rPolygonTypeControl(self, fullAttributeName):
        self.rPolygonTypeControlID = cmds.radioButtonGrp(
            label =                 "Type",
            annotation =            "",
            numberOfRadioButtons =  2,

            label1 =                "Convex",
            data1 =                 0,

            label2 =                "Star",
            data2 =                 1,

            changeCommand =         self._updateDimmingForRPolygon
        )

        self.rPolygonTypeControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   REGULAR POLYGON TYPE CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def rPolygonTypeControlConnect(self, fullAttributeName):
        cmds.connectControl(self.rPolygonTypeControlID, fullAttributeName)
        self.rPolygonTypeControlDimming()

    #-------------------------------------------------------------------------#
    #   REGULAR POLYGON TYPE CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def rPolygonTypeControlDimming(self):
        if self.rPolygonTypeControlID != None:
            if self.activeWireProfilesIndex == WireMeshCreatorNode.rPolygonWireProfileIndex:
                enableControl = True
            else:
                enableControl = False

            cmds.radioButtonGrp(
                self.rPolygonTypeControlID,
                edit =      True,
                enable =    enableControl                   
            )

    #-------------------------------------------------------------------------#
    #   REGULAR POLYGON SIDES CONTROL
    #-------------------------------------------------------------------------#
    def rPolygonSidesControl(self, fullAttributeName):
        self.rPolygonSidesControlID = cmds.intSliderGrp(
            label =                 "Sides",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultRPolygonSides,
            minValue =              WireMeshCreatorNode.minRPolygonSides,
            maxValue =              40,
            fieldMinValue =         WireMeshCreatorNode.minRPolygonSides,
            fieldMaxValue =         WireMeshCreatorNode.maxRPolygonSides
        )

        self.rPolygonSidesControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   REGULAR POLYGON SIDES CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def rPolygonSidesControlConnect(self, fullAttributeName):
        cmds.connectControl(self.rPolygonSidesControlID, fullAttributeName)
        self.rPolygonSidesControlDimming()

    #-------------------------------------------------------------------------#
    #   REGULAR POLYGON SIDES CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def rPolygonSidesControlDimming(self):
        if self.rPolygonSidesControlID != None:
            if self.activeWireProfilesIndex == WireMeshCreatorNode.rPolygonWireProfileIndex:
                enableControl = True
            else:
                enableControl = False

            cmds.intSliderGrp(
                self.rPolygonSidesControlID,
                edit =      True,
                enable =    enableControl                   
            )

    #-------------------------------------------------------------------------#
    #   REGULAR POLYGON INNER RADIUS CONTROL
    #-------------------------------------------------------------------------#
    def rPolygonInnerRadiusControl(self, fullAttributeName):
        self.rPolygonInnerRadiusControlID = cmds.floatSliderGrp(
            label =                 "Inner Radius",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultRPolygonInnerRadius,
            minValue =              WireMeshCreatorNode.minRPolygonInnerRadius,
            maxValue =              WireMeshCreatorNode.maxRPolygonInnerRadius
        )

        self.rPolygonInnerRadiusControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   REGULAR POLYGON INNER RADIUS CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def rPolygonInnerRadiusControlConnect(self, fullAttributeName):
        cmds.connectControl(self.rPolygonInnerRadiusControlID, fullAttributeName)
        self.rPolygonInnerRadiusControlDimming()

    #-------------------------------------------------------------------------#
    #   REGULAR POLYGON INNER RADIUS CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def rPolygonInnerRadiusControlDimming(self):
        if self.rPolygonTypeControlID != None and self.rPolygonInnerRadiusControlID != None:
            if self.activeWireProfilesIndex == WireMeshCreatorNode.rPolygonWireProfileIndex:
                rPolygonType = cmds.radioButtonGrp(     # first radio button is 1 (int)
                    self.rPolygonTypeControlID,
                    query =     True,
                    select =    True                    # returns what is currently selected
                )

                if rPolygonType == 2:       # star
                    enableControl = True
                else:                       # convex and others...
                    enableControl = False

            else:
                enableControl = False

            cmds.floatSliderGrp(
                self.rPolygonInnerRadiusControlID,
                edit =      True,
                enable =    enableControl
            )

    #-------------------------------------------------------------------------#
    #   PATTERN LAYOUT CONTROL
    #-------------------------------------------------------------------------#
    def patternLayoutControl(self, fullAttributeName):
        self.patternLayoutControlID = cmds.radioButtonGrp(
            label =                 "Layout",
            annotation =            "",
            numberOfRadioButtons =  2,

            label1 =                "Circle",
            data1 =                 0,

            label2 =                "Line",
            data2 =                 1
        )

        self.patternLayoutControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   PATTERN LAYOUT CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def patternLayoutControlConnect(self, fullAttributeName):
        cmds.connectControl(self.patternLayoutControlID, fullAttributeName)
        self.patternLayoutControlDimming()

    #-------------------------------------------------------------------------#
    #   PATTERN LAYOUT CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def patternLayoutControlDimming(self):
        if self.patternLayoutControlID != None:
            enableControl = cmds.getAttr(self.activeNodeName + "." + WireMeshCreatorNode.anPatternEnable)
            cmds.radioButtonGrp(
                self.patternLayoutControlID,
                edit =      True,
                enable =    enableControl
            )

    #-------------------------------------------------------------------------#
    #   PATTERN NUMBER OF SUBPROFILES CONTROL
    #-------------------------------------------------------------------------#
    def patternNumberOfSubprofilesControl(self, fullAttributeName):
        self.patternNumberOfSubprofilesControlID = cmds.intSliderGrp(
            label =                 "Number of Subprofiles",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultPatternNOS,
            minValue =              1,
            maxValue =              10,
            fieldMinValue =         WireMeshCreatorNode.minPatternNOS,
            fieldMaxValue =         WireMeshCreatorNode.maxPatternNOS
        )

        self.patternNumberOfSubprofilesControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   PATTERN NUMBER OF SUBPROFILES CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def patternNumberOfSubprofilesControlConnect(self, fullAttributeName):
        cmds.connectControl(self.patternNumberOfSubprofilesControlID, fullAttributeName)
        self.patternNumberOfSubprofilesControlDimming()

    #-------------------------------------------------------------------------#
    #   PATTERN NUMBER OF SUBPROFILES CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def patternNumberOfSubprofilesControlDimming(self):
        if self.patternNumberOfSubprofilesControlID != None:
            enableControl = cmds.getAttr(self.activeNodeName + "." + WireMeshCreatorNode.anPatternEnable)
            cmds.intSliderGrp(
                self.patternNumberOfSubprofilesControlID,
                edit =      True,
                enable =    enableControl
            )

    #-------------------------------------------------------------------------#
    #   PATTERN SCALE SUBPROFILES CONTROL
    #-------------------------------------------------------------------------#
    def patternScaleSubprofilesControl(self, fullAttributeName):
        self.patternScaleSubprofilesControlID = cmds.floatSliderGrp(
            label =                 "Scale Subprofiles",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultPatternScaleSubprofiles,
            minValue =              WireMeshCreatorNode.minPatternScaleSubprofiles,
            maxValue =              4.0,
            fieldMinValue =         WireMeshCreatorNode.minPatternScaleSubprofiles,
            fieldMaxValue =         WireMeshCreatorNode.maxPatternScaleSubprofiles
        )

        self.patternScaleSubprofilesControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   PATTERN SCALE SUBPROFILES CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def patternScaleSubprofilesControlConnect(self, fullAttributeName):
        cmds.connectControl(self.patternScaleSubprofilesControlID, fullAttributeName)
        self.patternScaleSubprofilesControlDimming()

    #-------------------------------------------------------------------------#
    #   PATTERN SCALE SUBPROFILES CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def patternScaleSubprofilesControlDimming(self):
        if self.patternScaleSubprofilesControlID != None:
            enableControl = cmds.getAttr(self.activeNodeName + "." + WireMeshCreatorNode.anPatternEnable)
            cmds.floatSliderGrp(
                self.patternScaleSubprofilesControlID,
                edit =      True,
                enable =    enableControl
            )

    #-------------------------------------------------------------------------#
    #   PATTERN COVERAGE CONTROL
    #-------------------------------------------------------------------------#
    def patternCoverageControl(self, fullAttributeName):
        self.patternCoverageControlID = cmds.floatSliderGrp(
            label =                 "Coverage",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultPatternCoverage,
            minValue =              WireMeshCreatorNode.minPatternCoverage,
            maxValue =              WireMeshCreatorNode.maxPatternCoverage,
        )

        self.patternCoverageControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   PATTERN COVERAGE CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def patternCoverageControlConnect(self, fullAttributeName):
        cmds.connectControl(self.patternCoverageControlID, fullAttributeName)
        self.patternCoverageControlDimming()

    #-------------------------------------------------------------------------#
    #   PATTERN COVERAGE CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def patternCoverageControlDimming(self):
        if self.patternCoverageControlID != None:
            enableControl = cmds.getAttr(self.activeNodeName + "." + WireMeshCreatorNode.anPatternEnable)
            cmds.floatSliderGrp(
                self.patternCoverageControlID,
                edit =      True,
                enable =    enableControl
            )

    #-------------------------------------------------------------------------#
    #   INTERPOLATION STEPS CONTROL
    #-------------------------------------------------------------------------#
    def interpolationStepsControl(self, fullAttributeName):
        self.iterpolationStepsControlID = cmds.intSliderGrp(
            label =                 "Steps",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultInterpolationSteps,
            minValue =              WireMeshCreatorNode.minInterpolationSteps,
            maxValue =              50,
            fieldMinValue =         WireMeshCreatorNode.minInterpolationSteps,
            fieldMaxValue =         1000000
        )

        self.interpolationStepsControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   INTERPOLATION STEPS CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def interpolationStepsControlConnect(self, fullAttributeName):
        cmds.connectControl(self.iterpolationStepsControlID, fullAttributeName)
        self.interpolationStepsControlDimming()

    #-------------------------------------------------------------------------#
    #   INTERPOLATION STEPS CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def interpolationStepsControlDimming(self):
        if self.iterpolationStepsControlID != None:
            interpolationRange = cmds.getAttr(self.activeNodeName + "." + WireMeshCreatorNode.anInterpolationRange)
            if interpolationRange != 2:
                enableControl = True
            else:
                 enableControl = False

            cmds.intSliderGrp(
                self.iterpolationStepsControlID,
                edit =      True,
                enable =    enableControl
            )

    #-------------------------------------------------------------------------#
    #   INTERPOLATION DISTANCE CONTROL
    #-------------------------------------------------------------------------#
    def interpolationDistanceControl(self, fullAttributeName):
        self.iterpolationDistanceControlID = cmds.floatSliderGrp(
            label =                 "Distance",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultInterpolationDistance,
            minValue =              0.5,
            maxValue =              10.0,
            fieldMinValue =         WireMeshCreatorNode.minInterpolationDistance,
            fieldMaxValue =         10000.0
        )

        self.interpolationDistanceControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   INTERPOLATION DISTANCE CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def interpolationDistanceControlConnect(self, fullAttributeName):
        cmds.connectControl(self.iterpolationDistanceControlID, fullAttributeName)
        self.interpolationDistanceControlDimming()

    #-------------------------------------------------------------------------#
    #   INTERPOLATION DISTANCE CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def interpolationDistanceControlDimming(self):
        if self.iterpolationDistanceControlID != None:
            interpolationRange = cmds.getAttr(self.activeNodeName + "." + WireMeshCreatorNode.anInterpolationRange)
            if interpolationRange == 2:
                enableControl = True
            else:
                 enableControl = False

            cmds.floatSliderGrp(
                self.iterpolationDistanceControlID,
                edit =      True,
                enable =    enableControl
            )

    #-------------------------------------------------------------------------#
    #   SCALE PROFILE CONTROL
    #-------------------------------------------------------------------------#
    def scaleProfileControl(self, fullAttributeName):
        self.scaleProfileControlID = cmds.floatSliderGrp(
            label =                 "Scale Profile",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultScaleProfile,
            minValue =              WireMeshCreatorNode.minScaleProfile,
            maxValue =              10.0,
            fieldMinValue =         WireMeshCreatorNode.minScaleProfile,
            fieldMaxValue =         WireMeshCreatorNode.maxScaleProfile
        )

        self.scaleProfileControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   INTERPOLATION STEPS CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def scaleProfileControlConnect(self, fullAttributeName):
        cmds.connectControl(self.scaleProfileControlID, fullAttributeName)

    #-------------------------------------------------------------------------#
    #   ROTATE PROFILE CONTROL
    #-------------------------------------------------------------------------#
    def rotateProfileControl(self, fullAttributeName):
        self.rotateProfileControlID = cmds.floatSliderGrp(
            label =                 "Rotate Profile",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultRotateProfile,
            minValue =              WireMeshCreatorNode.minRotateProfile,
            maxValue =              WireMeshCreatorNode.maxRotateProfile
        )

        self.rotateProfileControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   ROTATE STEPS CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def rotateProfileControlConnect(self, fullAttributeName):
        cmds.connectControl(self.rotateProfileControlID, fullAttributeName)

    #-------------------------------------------------------------------------#
    #   TWIST CONTROL
    #-------------------------------------------------------------------------#
    def twistControl(self, fullAttributeName):
        self.twistControlID = cmds.floatSliderGrp(
            label =                 "Twist",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultTwist,
            minValue =              0.0,
            maxValue =              1800.0,
            fieldMinValue =         -10000000.0,
            fieldMaxValue =         10000000.0,
        )

        self.twistControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   TWIST CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def twistControlConnect(self, fullAttributeName):
        cmds.connectControl(self.twistControlID, fullAttributeName)

    #-------------------------------------------------------------------------#
    #   NORMALS SMOOTHING CONTROL
    #-------------------------------------------------------------------------#
    def normalsSmoothingControl(self, fullAttributeName):
        self.normalsSmoothingControlID = cmds.floatSliderGrp(
            label =                 "Smoothing",
            annotation =            "",
            field =                 True,
            value =                 WireMeshCreatorNode.defaultNormalsSmoothing,
            minValue =              WireMeshCreatorNode.minNormalsSmoothing,
            maxValue =              WireMeshCreatorNode.maxNormalsSmoothing
        )

        self.normalsSmoothingControlConnect(fullAttributeName)

    #-------------------------------------------------------------------------#
    #   NORMALS SMOOTHING CONTROL CONNECT
    #-------------------------------------------------------------------------#
    def normalsSmoothingControlConnect(self, fullAttributeName):
        cmds.connectControl(self.normalsSmoothingControlID, fullAttributeName)

    #-------------------------------------------------------------------------#
    #   _ UPDATE DIMMING FOR REGULAR POLYGON
    #-------------------------------------------------------------------------#
    def _updateDimmingForRPolygon(self, *args):
        self.rPolygonTypeControlDimming()
        self.rPolygonSidesControlDimming()
        self.rPolygonInnerRadiusControlDimming()

    #-------------------------------------------------------------------------#
    #   _ UPDATE DIMMING FOR PATTERN
    #-------------------------------------------------------------------------#
    def _updateDimmingForPattern(self, *args):
        self.patternLayoutControlDimming()
        self.patternNumberOfSubprofilesControlDimming()
        self.patternScaleSubprofilesControlDimming()
        self.patternCoverageControlDimming()

    #-------------------------------------------------------------------------#
    #   _ UPDATE DIMMING FOR INTERPOLATION
    #-------------------------------------------------------------------------#
    def _updateDimmingForInterpolation(self, *args):
        self.interpolationStepsControlDimming()
        self.interpolationDistanceControlDimming()

    #-------------------------------------------------------------------------#
    #   _ PATTERN ENABLE CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def _patternEnableControlDimming(self, nodeName):
        if self.activeWireProfilesIndex == WireMeshCreatorNode.customWireProfileIndex:
            dimControl = True
        else:
            dimControl = False

        self.dimControl(nodeName, WireMeshCreatorNode.anPatternEnable, dimControl)

        self._updateDimmingForPattern()

    #-------------------------------------------------------------------------#
    #   _ INTERPOLATION RANGE CONTROL DIMMING
    #-------------------------------------------------------------------------#
    def _interpolationRangeControlDimming(self, nodeName):
        self._updateDimmingForInterpolation()

    #-------------------------------------------------------------------------#
    #   _ SELECT WIRE PROFILES
    #-------------------------------------------------------------------------#
    def _selectWireProfiles(self, fullAttributeName, wireProfileShapeIndex, *args):
        self.activeWireProfilesIndex = wireProfileShapeIndex
        
        self._resetWireProfilesControls()
        self._highlightWireProfilesControls(wireProfileShapeIndex)

        self._updateDimmingForRPolygon()
        self._updateDimmingForPattern()

        cmds.setAttr(fullAttributeName, wireProfileShapeIndex)

    #-------------------------------------------------------------------------#
    #   _ RESET WIRE PROFILES CONTROLS
    #-------------------------------------------------------------------------#
    def _resetWireProfilesControls(self):
        for (key, value) in self.wireProfilesControlsMap.items():
            cmds.symbolButton(
                value[0], 
                edit =              True,
                enableBackground =  False
            )                
            cmds.text(
                value[1],
                edit =              True,
                backgroundColor =   AEwireMeshCreatorTemplate.textBackgroundColorInactive,
                highlightColor =    (255.0/255.0, 255.0/255.0, 255.0/255.0)  
            )

    #-------------------------------------------------------------------------#
    #   _ HIGHLIGHT WIRE PROFILES CONTROLS
    #-------------------------------------------------------------------------#
    def _highlightWireProfilesControls(self, wireProfileShapeIndex):
        (buttonID, textID) = self.wireProfilesControlsMap[wireProfileShapeIndex]
        cmds.symbolButton(
            buttonID, 
            edit =              True,
            enableBackground =  True,
            backgroundColor =   AEwireMeshCreatorTemplate.imageBackgroundColorActive
        )                
        cmds.text(
            textID,
            edit =              True,
            backgroundColor =   AEwireMeshCreatorTemplate.textBackgroundColorActive,
            highlightColor =    (255.0/255.0, 56.0/255.0, 56.0/255.0)  
        )

    #-------------------------------------------------------------------------#
    #   ATTRIBUTE EDITOR TEMPLATE CREATOR
    #-------------------------------------------------------------------------#
    @staticmethod
    def aeTemplateCreator(nodeName):
        return AEwireMeshCreatorTemplate(nodeName)

