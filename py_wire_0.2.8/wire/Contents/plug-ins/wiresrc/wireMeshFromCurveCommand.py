#-------------------------------------------------------------------------#
#   CREATED:
#       14 VIII 2017
#   INFO:
#       ...
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
#   IMPORTS
#-------------------------------------------------------------------------#
from maya.api.OpenMaya import MArgDatabase
from maya.api.OpenMaya import MDagModifier
from maya.api.OpenMaya import MDGModifier
from maya.api.OpenMaya import MGlobal
from maya.api.OpenMaya import MPlug
from maya.api.OpenMaya import MSelectionList
from maya.api.OpenMaya import MSyntax

from maya.api.OpenMaya import MFn
from maya.api.OpenMaya import MFnDagNode
from maya.api.OpenMaya import MFnDependencyNode
from maya.api.OpenMaya import MFnSet

from maya.api.OpenMaya import MPxCommand

import maya.cmds as cmds
import pymel.core as pm

from wireMeshCreatorNode import WireMeshCreatorNode

#-------------------------------------------------------------------------#
#   CLASS DEFINITIONS
#   WIRE MESH FROM CURVE COMMAND
#-------------------------------------------------------------------------#
class WireMeshFromCurveCommand(MPxCommand):
    #-------------------------------------------------------------------------#
    #   STATIC CLASS MEMBERS
    #-------------------------------------------------------------------------#
    # COMMAND INFORMATIONS
    commandName =           "wireMeshFromCurve"

    # FLAGS
    flsOneNodePerCurve =    "-onc"
    fllOneNodePerCurve =    "-oneNodePerCurve"

    #-------------------------------------------------------------------------#
    #   CONSTRUCTOR
    #-------------------------------------------------------------------------#
    def __init__(self, *args, **kwargs):
        # INITIALIZE
        super(WireMeshFromCurveCommand, self).__init__(*args, **kwargs)

        self.oneNodePerCurve =      False

    #-------------------------------------------------------------------------#
    #   IS UNDOABLE
    #-------------------------------------------------------------------------#
    def isUndoable(self):
        return True

    #-------------------------------------------------------------------------#
    #   DO IT
    #-------------------------------------------------------------------------#
    def doIt(self, argList):
        #-------------------------------------------------------------------------#
        #   PARSE ARGUMENTS
        #-------------------------------------------------------------------------#
        argDatabase = MArgDatabase(self.syntax(), argList)

        # FLAG ARGUMENTS
        # one node per curve
        if argDatabase.isFlagSet(WireMeshFromCurveCommand.flsOneNodePerCurve) == True:
            self.oneNodePerCurve = argDatabase.flagArgumentBool(
                WireMeshFromCurveCommand.flsOneNodePerCurve, 0)
        elif argDatabase.isFlagSet(WireMeshFromCurveCommand.fllOneNodePerCurve) == True:
            self.oneNodePerCurve = argDatabase.flagArgumentBool(
                WireMeshFromCurveCommand.fllOneNodePerCurve, 0)

        # COMMAND OBJECTS
        self.selectionList =    argDatabase.getObjectList()
        self.curveNodeList =    []

        if self.selectionList.length() == 0:
            MGlobal.displayError("Select curves before calling this command!")
            return
        else:
            for i in range(self.selectionList.length()):
                dagPath = self.selectionList.getDagPath(i)
                dagPath.extendToShape()
                
                if (dagPath.apiType() != MFn.kNurbsCurve):
                    MGlobal.displayError("All selected objects should be curves!")
                    return

                self.curveNodeList.append(dagPath.node())

        #-------------------------------------------------------------------------#
        #   EXECUTE
        #-------------------------------------------------------------------------#
        self.redoIt()

    #-------------------------------------------------------------------------#
    #   REDO IT
    #-------------------------------------------------------------------------#
    def redoIt(self):
        self.dgModifier =     MDGModifier()
        self.dagModifier =    MDagModifier()

        # CREATE NODES
        self.wireMeshCreatorNodeList =   []
        self.wireMeshNodeList =          []

        # wire mesh creator node
        numWireMeshCreatorNodes = 0
        if self.oneNodePerCurve == True:
            numWireMeshCreatorNodes = self.selectionList.length()
        else:
            numWireMeshCreatorNodes = 1

        for i in range(numWireMeshCreatorNodes):
            oWireMeshCreatorNode = self.dgModifier.createNode(WireMeshCreatorNode.nodeName)
            self.wireMeshCreatorNodeList.append(oWireMeshCreatorNode)
        
        self.dgModifier.doIt()

        # mesh and transform nodes
        for i in range(self.selectionList.length()):
            oWireTransformNode =    self.dagModifier.createNode("transform")
            oWireMeshNode =         self.dagModifier.createNode("mesh", oWireTransformNode)

            self.dagModifier.renameNode(oWireTransformNode, "wire#")
            self.dagModifier.renameNode(oWireMeshNode, "wireShape#")

            self.wireMeshNodeList.append(oWireMeshNode)

        self.dagModifier.doIt()

        # CONNECT ATTRIBUTES
        fnDependencyNode =  MFnDependencyNode()
        for i in range(len(self.curveNodeList)):
            # CONNECT worldSpace (CURVE NODE) TO inCurveArray (WIRE MESH CREATOR NODE)
            # worldSpace
            fnDependencyNode.setObject(self.curveNodeList[i])
            pWorldSpace = fnDependencyNode.findPlug("worldSpace", False)
            pWorldSpace.selectAncestorLogicalIndex(0, pWorldSpace.attribute())

            # inCurveArray
            # We could use MPlug constructor and pass WireMeshCreatorNode.aInCurveArray
            # but because I heavly rely on reloading python modules for this plugin 
            # during Maya session for testing purposes (so I don't have to reopen Maya 
            # every time I make some changes in plugin's code) this isn't an option 
            # - static class members will be resetted to initial values (in this case 
            # node attributes will be resetted to empty MObjects).
            # pInCurveArray = MPlug(
            #     self.wireMeshCreatorNodeList[0], 
            #     WireMeshCreatorNode.aInCurveArray)
            pInCurveArray = MPlug()
            if self.oneNodePerCurve == True:
                fnDependencyNode.setObject(self.wireMeshCreatorNodeList[i])
                pInCurveArray = fnDependencyNode.findPlug("inCurveArray", False)
                pInCurveArray.selectAncestorLogicalIndex(0, pInCurveArray.attribute())  # create new plug at logical index i
            else:
                fnDependencyNode.setObject(self.wireMeshCreatorNodeList[0])
                pInCurveArray = fnDependencyNode.findPlug("inCurveArray", False)
                pInCurveArray.selectAncestorLogicalIndex(i, pInCurveArray.attribute())  # create new plug at logical index i

            # connect
            self.dgModifier.connect(pWorldSpace, pInCurveArray)
            self.dgModifier.doIt()

            # CONNECT ourMeshArray (WIRE MESH CREATOR NODE) TO inMesh (MESH NODE)
            # outMeshArray
            pOutMeshArray = MPlug()
            if self.oneNodePerCurve == True:
                fnDependencyNode.setObject(self.wireMeshCreatorNodeList[i])
                pOutMeshArray = fnDependencyNode.findPlug("outMeshArray", False)
                pOutMeshArray.selectAncestorLogicalIndex(0, pOutMeshArray.attribute())  # create new plug at logical index i
            else:
                fnDependencyNode.setObject(self.wireMeshCreatorNodeList[0])
                pOutMeshArray = fnDependencyNode.findPlug("outMeshArray", False)
                pOutMeshArray.selectAncestorLogicalIndex(i, pOutMeshArray.attribute())  # create new plug at logical index i

            # inMesh
            fnDependencyNode.setObject(self.wireMeshNodeList[i])
            pInMesh = fnDependencyNode.findPlug("inMesh", False)

            # connect
            self.dgModifier.connect(pOutMeshArray, pInMesh)
            self.dgModifier.doIt()

        # ASSIGN DEFAULT MAYA SHADER TO MESH NODES
        fnDAGNode = MFnDagNode()
        for oWireMeshNode in self.wireMeshNodeList:
            fnDAGNode.setObject(oWireMeshNode)
            self.dgModifier.commandToExecute(
                "sets -addElement initialShadingGroup " + fnDAGNode.fullPathName())

        self.dgModifier.doIt()

        # SELECT LAST WIRE MESH CREATOR NODE AND SHOW IT IN ATTRIBUTE EDITOR
        fnDependencyNode.setObject(self.wireMeshCreatorNodeList[-1])
        self.dgModifier.commandToExecute(
                "select -replace " + fnDependencyNode.absoluteName())
        self.dgModifier.doIt()

        cmds.workspaceControl("AttributeEditor", edit=True, restore=True)

    #-------------------------------------------------------------------------#
    #   UNDO IT
    #-------------------------------------------------------------------------#
    def undoIt(self):
        self.dgModifier.undoIt()
        self.dagModifier.undoIt()

    #-------------------------------------------------------------------------#
    #   INVOKE
    #-------------------------------------------------------------------------#
    @staticmethod
    def invoke(*args, **kwargs):
        pm.mel.eval(WireMeshFromCurveCommand.commandName)   # calling: cmds.wireMeshFromCurve()

    #-------------------------------------------------------------------------#
    #   COMMAND SYNTAX
    #-------------------------------------------------------------------------#
    @staticmethod
    def commandSyntax():
        syntax = MSyntax()

        # FLAG ARGUMENTS
        syntax.addFlag(
            WireMeshFromCurveCommand.flsOneNodePerCurve,
            WireMeshFromCurveCommand.fllOneNodePerCurve,
            MSyntax.kBoolean
        )

        # COMMAND OBJECTS
        syntax.useSelectionAsDefault(True)
        syntax.setObjectType(MSyntax.kSelectionList, 0)

        # OTHER 
        syntax.enableEdit = False
        syntax.enableQuery = False

        return syntax

    #-------------------------------------------------------------------------#
    #   COMMAND CREATOR
    #-------------------------------------------------------------------------#
    @staticmethod
    def commandCreator():
        return WireMeshFromCurveCommand()
