#include "moleculeCmd.h"
#include "moleculeNode.h"
#include <maya/MArgDatabase.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MItSelectionList.h>
#include <maya/MObject.h>
#include <maya/MPlug.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MArgDatabase.h>
#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnTransform.h>
#include <maya/MFn.h>
#include <maya/MSyntax.h>
#include <maya/MDistance.h>

const char *radiusFlag = "-r", *radiusLongFlag = "-radius";
const char *segsFlag = "-s", *segsLongFlag = "-segments";
const char *ballRatioFlag = "-br", *ballRatioLongFlag = "-ballRatio";

MStatus MoleculeCmd::doIt(const MArgList& args)
{
	MStatus stat;

	radius = MoleculeNode::radiusDefault();
	segs = MoleculeNode::segmentsDefault();
	ballRodRatio = MoleculeNode::ballRatioDefault();

	moleculeNodes.clear();
	meshShapeNodes.clear();

	MArgDatabase argData(syntax(), args, &stat);
	if (!stat)
	{
		return stat;
	}

	if (argData.isFlagSet(radiusFlag))
	{
		argData.getFlagArgument(radiusFlag, 0, radius);
	}
	if (argData.isFlagSet(segsFlag))
	{
		argData.getFlagArgument(segsFlag, 0, segs);
	}
	if (argData.isFlagSet(ballRatioFlag))
	{
		argData.getFlagArgument(ballRatioFlag, 0, ballRodRatio);
	}

	MSelectionList selection;
	MGlobal::getActiveSelectionList(selection);

	MObject inMeshShape;
	MPlug outMeshPlug, inMeshPlug;
	MFnDependencyNode nodeFn, moleculeNodeFn;
	MObject moleculeNode, newMeshTransform, newMeshShape;
	MFnDagNode dagFn;

	int nSelMeshes = 0;
	MDagPath dagPath;
	MItSelectionList iter(selection, MFn::kMesh);
	for (; !iter.isDone(); iter.next())
	{
		nSelMeshes++;
		iter.getDagPath(dagPath);

		// get shape node
		dagPath.extendToShape();
		inMeshShape = dagPath.node();

		dagFn.setObject(dagPath);
		unsigned int instanceNum = dagPath.instanceNumber();
		MPlug outMeshesPlug = dagFn.findPlug("worldMesh");
		outMeshPlug = outMeshesPlug.elementByLogicalIndex(instanceNum);
		
		moleculeNode = dagMods[0].createNode(MoleculeNode::id);
		moleculeNodes.append(moleculeNode);
		moleculeNodeFn.setObject(moleculeNode);

		MPlug inMeshPlug = moleculeNodeFn.findPlug("inMesh");
		dagMods[0].connect(outMeshPlug, inMeshPlug);

		newMeshTransform = dagMods[0].createNode("transform");
		newMeshShape = dagMods[0].createNode("mesh", newMeshTransform);
		meshShapeNodes.append(newMeshShape);

		dagMods[0].renameNode(newMeshTransform, "molecule");

		nodeFn.setObject(newMeshShape);

		outMeshPlug = moleculeNodeFn.findPlug("outMesh", &stat);
		inMeshPlug = nodeFn.findPlug("inMesh", &stat);
		stat = dagMods[0].connect(outMeshPlug, inMeshPlug);
	}

	if (nSelMeshes == 0)
	{
		MGlobal::displayWarning("Select one or more meshes");
		return MS::kFailure;
	}

	dagMods[0].doIt();

	unsigned int i;
	for ( i = 0; i < moleculeNodes.length(); i++)
	{
		nodeFn.setObject(moleculeNodes[i]);
		dagMods[1].commandToExecute(MString("setAttr ") + nodeFn.name() + ".radius " + radius.value());
		dagMods[1].commandToExecute(MString("setAttr ") + nodeFn.name() + ".segments " + segs);
		dagMods[1].commandToExecute(MString("setAttr ") + nodeFn.name() + ".ballRatio " + ballRodRatio);
	}

	// 给形状节点赋材质
	for ( i = 0; i < meshShapeNodes.length(); i++)
	{
		nodeFn.setObject(meshShapeNodes[i]);
		dagMods[1].commandToExecute(MString("sets -e -fe initialShadingGroup ") + nodeFn.name());
	}

	MString cmd("select -r");
	for ( i = 0; i < moleculeNodes.length(); i++)
	{
		nodeFn.setObject(moleculeNodes[i]);
		cmd += " " + nodeFn.name();
	}

	dagMods[1].commandToExecute(cmd);
	dagMods[1].doIt();

	return MS::kSuccess;
}

MStatus MoleculeCmd::redoIt()
{
	for (size_t i = 0; i < 2; i++)
	{
		dagMods[i].doIt();
	}

	return MS::kSuccess;
}

MStatus MoleculeCmd::undoIt()
{
	for (size_t i = 1; i >= 0; i--)
	{
		dagMods[i].undoIt();
	}

	return MS::kSuccess;
}

MSyntax MoleculeCmd::newSyntax()
{
	MSyntax syntax;
	
	syntax.addFlag(radiusFlag, radiusLongFlag, MSyntax::kDistance);
	syntax.addFlag(segsFlag, segsLongFlag, MSyntax::kLong);
	syntax.addFlag(ballRatioFlag, ballRatioLongFlag, MSyntax::kDouble);

	syntax.enableQuery(false);
	syntax.enableEdit(false);

	return syntax;
}
