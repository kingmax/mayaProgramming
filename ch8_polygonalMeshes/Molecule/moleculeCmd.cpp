#include "moleculeCmd.h"
#include "moleculeUtils.h"

#include <maya/MSelectionList.h>
#include <maya/MItSelectionList.h>
#include <maya/MGlobal.h>
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MPointArray.h>
#include <maya/MPoint.h>
#include <maya/MIntArray.h>
#include <maya/MObject.h>
#include <maya/MItMeshEdge.h>
#include <maya/MFn.h>
#include <maya/MFnMesh.h>



MStatus MoleculeCmd::doIt(const MArgList& args)
{
	double radius = 0.1;
	int segs = 6;
	double ballRodRatio = 2.0;
	MStatus stat;
	MSelectionList selection;
	MGlobal::getActiveSelectionList(selection);

	MDagPath dagPath;
	MFnMesh meshFn;

	int nBallPolys;
	MPointArray ballVerts;
	MIntArray ballPolyCounts;
	MIntArray ballPolyConnects;
	genBall(MPoint::origin, ballRodRatio * radius, segs, nBallPolys, ballVerts, ballPolyCounts, ballPolyConnects);
	
	unsigned int i, j, vertOffset;
	MPointArray meshVerts;
	MPoint p0, p1;
	MObject objTransform;

	int nRodPolys;
	MPointArray rodVerts;
	MIntArray rodPolyCounts;
	MIntArray rodPolyConnects;

	int nNewPolys;
	MPointArray newVerts;
	MIntArray newPolyCounts;
	MIntArray newPolyConnects;

	MItSelectionList iter(selection, MFn::kMesh);
	for (; !iter.isDone(); iter.next())
	{
		iter.getDagPath(dagPath);
		meshFn.setObject(dagPath);

		nNewPolys = 0;
		newVerts.clear();
		newPolyCounts.clear();
		newPolyConnects.clear();

		meshFn.getPoints(meshVerts);
		for (i = 0; i < meshVerts.length(); i++)
		{
			vertOffset = newVerts.length();
			nNewPolys += nBallPolys;

			for ( j = 0; j < ballVerts.length(); j++)
			{
				newVerts.append(meshVerts[i] + ballVerts[j]);
			}
			for ( j = 0; j < ballPolyCounts.length(); j++)
			{
				newPolyCounts.append(ballPolyCounts[j]);
			}
			for ( j = 0; j < ballPolyConnects.length(); j++)
			{
				newPolyConnects.append(vertOffset + ballPolyConnects[j]);
			}
		}

		MItMeshEdge edgeIter(dagPath);
		for (; !edgeIter.isDone(); edgeIter.next())
		{
			p0 = edgeIter.point(0);
			p1 = edgeIter.point(1);

			genRod(p0, p1, radius, segs, nRodPolys, rodVerts, rodPolyCounts, rodPolyConnects);

			vertOffset = newVerts.length();

			nNewPolys += nRodPolys;

			for ( i = 0; i < rodVerts.length(); i++)
			{
				newVerts.append(rodVerts[i]);
			}
			for ( i = 0; i < rodPolyCounts.length(); i++)
			{
				newPolyCounts.append(rodPolyCounts[i]);
			}
			for ( i = 0; i < rodPolyConnects.length(); i++)
			{
				newPolyConnects.append(vertOffset + rodPolyConnects[i]);
			}
		}

		objTransform = meshFn.create(newVerts.length(), nNewPolys, newVerts, newPolyCounts, newPolyConnects, MObject::kNullObj, &stat);

		if (!stat)
		{
			stat.perror("Unable to create mesh");
		}

		meshFn.updateSurface();

		MString cmd("sets -e -fe initialShadingGroup ");
		cmd += meshFn.name();
		MGlobal::executeCommand(cmd);
	}

	return MS::kSuccess;
}