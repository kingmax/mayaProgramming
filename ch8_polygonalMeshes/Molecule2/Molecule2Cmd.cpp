#include "utils.h"

#include <maya/MPxCommand.h>
#include <maya/MStatus.h>
#include <maya/MSyntax.h>
#include <maya/MDistance.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>
#include <maya/MSelectionList.h>
#include <maya/MGlobal.h>
#include <maya/MItSelectionList.h>
#include <maya/MFnMesh.h>
#include <maya/MItMeshEdge.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MDagModifier.h>

class Molecule2Cmd : public MPxCommand
{
public:
	virtual MStatus doIt(const MArgList&);
	virtual MStatus redoIt();
	virtual MStatus undoIt();
	virtual bool isUndoable() const;

	static void *creator();
	static MSyntax newSyntax();

private:
	MDistance radius;
	int segs;
	double ballRodRatio;
	MDagPathArray selMeshes;
	MObjectArray objTransforms;
};

const char *radiusFlag = "-r", *radiusLongFlag = "-radius";
const char *segsFlag = "-s", *segsLongFlag = "-segments";
const char *ballRatioFlag = "-br", *ballRatioLongFlag = "-ballRatio";

bool Molecule2Cmd::isUndoable() const { return true; }

void *Molecule2Cmd::creator() { return new Molecule2Cmd(); }

MSyntax Molecule2Cmd::newSyntax()
{
	MSyntax syntax;

	syntax.addFlag(radiusFlag, radiusLongFlag, MSyntax::kDistance);
	syntax.addFlag(segsFlag, segsLongFlag, MSyntax::kLong);
	syntax.addFlag(ballRatioFlag, ballRatioLongFlag, MSyntax::kDouble);

	syntax.enableEdit(false);
	syntax.enableQuery(false);

	return syntax;
}

MStatus Molecule2Cmd::doIt(const MArgList &args)
{
	MStatus stat;

	radius.setValue(0.1);
	segs = 6;
	ballRodRatio = 2.0;
	selMeshes.clear();

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

	MDagPath dagPath;
	MItSelectionList iter(selection, MFn::kMesh);
	for (; !iter.isDone(); iter.next())
	{
		iter.getDagPath(dagPath);
		selMeshes.append(dagPath);
	}

	if (selMeshes.length() == 0)
	{
		MGlobal::displayWarning("Select one or more meshes");
		return MS::kFailure;
	}

	return redoIt();
}


MStatus Molecule2Cmd::redoIt()
{
	MStatus stat;
	MDagPath dagPath;
	MFnMesh meshFn;

	int nBallPolys;
	MPointArray ballVerts;
	MIntArray ballPolyCounts;
	MIntArray ballPolyConnects;
	MFloatArray ballUCoords;
	MFloatArray ballVCoords;
	MIntArray ballFvUVIDs;
	genBall(MPoint::origin, ballRodRatio * radius.value(), segs, nBallPolys, ballVerts, ballPolyCounts, ballPolyConnects, true, ballUCoords, ballVCoords, ballFvUVIDs);

	unsigned int i, j, vertOffset;
	MPointArray meshVerts;
	MPoint p0, p1;
	MObject objTransform;

	int nRodPolys;
	MPointArray rodVerts;
	MIntArray rodPolyCounts;
	MIntArray rodPolyConnects;
	MFloatArray rodUCoords;
	MFloatArray rodVCoords;
	MIntArray rodFvUVIDs;

	int nNewPolys;
	MPointArray newVerts;
	MIntArray newPolyCounts;
	MIntArray newPolyConnects;
	MFloatArray newUCoords;
	MFloatArray newVCoords;
	MIntArray newFvUVIDs;

	int uvOffset;
	MDagModifier dagMod;
	MFnDagNode dagFn;

	objTransforms.clear();

	unsigned int mi;
	for ( mi = 0; mi < selMeshes.length(); mi++)
	{
		dagPath = selMeshes[mi];
		meshFn.setObject(dagPath);

		uvOffset = 0;
		nNewPolys = 0;
		newVerts.clear();
		newPolyCounts.clear();
		newPolyConnects.clear();
		newUCoords.clear();
		newVCoords.clear();
		newFvUVIDs.clear();

		// 得到每个选择物体的点坐标 -> meshVerts
		meshFn.getPoints(meshVerts, MSpace::kWorld);
		for ( i = 0; i < meshVerts.length(); i++)
		{
			// get newVerts index while append new data, [].extents or [].append
			// 从哪个位置插入新数据？
			vertOffset = newVerts.length();
			nNewPolys += nBallPolys;

			// new verts array
			for (j = 0; j < ballVerts.length(); j++)
				newVerts.append(meshVerts[i] + ballVerts[j]);
			
			// new face array
			for (j = 0; j < ballPolyCounts.length(); j++)
				newPolyCounts.append(ballPolyCounts[j]);

			// new face connect array ???
			for (j = 0; j < ballPolyConnects.length(); j++)
				newPolyConnects.append(vertOffset + ballPolyConnects[j]);

			// first vertex
			// 一次性插入所有UV坐标
			if (i == 0)
			{
				for (j = 0; j < ballUCoords.length(); j++)
				{
					newUCoords.append(ballUCoords[j]);
					newVCoords.append(ballVCoords[j]);
				}
			}

			// Face-Vertex UV ID array
			for (j = 0; j < ballFvUVIDs.length(); j++)
				newFvUVIDs.append(uvOffset + ballFvUVIDs[j]);	//??? uvOffset=0? change to newFvUVIDs.append(ballFvUVIDs[j])?
		}

		uvOffset = newUCoords.length();

		int nRods = 0;
		MItMeshEdge edgeIter(dagPath);
		// 遍历边，创建球
		for (; !edgeIter.isDone(); edgeIter.next(), nRods++)
		{
			p0 = edgeIter.point(0, MSpace::kWorld);
			p1 = edgeIter.point(1, MSpace::kWorld);

			genRod(p0, p1,
				radius.value(), segs, nRodPolys,
				rodVerts, rodPolyCounts, rodPolyConnects,
				nRods == 0, rodUCoords, rodVCoords, rodFvUVIDs);


		}
	}
}