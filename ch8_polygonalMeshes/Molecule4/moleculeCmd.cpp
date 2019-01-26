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

	}
}