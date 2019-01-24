#include "utils.h"
#include "molecule2Cmd.h"

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
		// 遍历顶点，创建球
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
		// 遍历边，创建连接件
		for (; !edgeIter.isDone(); edgeIter.next(), nRods++)
		{
			p0 = edgeIter.point(0, MSpace::kWorld);
			p1 = edgeIter.point(1, MSpace::kWorld);

			genRod(p0, p1,
				radius.value(), segs, nRodPolys,
				rodVerts, rodPolyCounts, rodPolyConnects,
				nRods == 0, rodUCoords, rodVCoords, rodFvUVIDs);

			vertOffset = newVerts.length();
			nNewPolys += nRodPolys;

			for (i = 0; i < rodVerts.length(); i++)
				newVerts.append(rodVerts[i]);
			for (i = 0; i < rodPolyCounts.length(); i++)
				newPolyCounts.append(rodPolyCounts[i]);
			for (i = 0; i < rodPolyConnects.length(); i++)
				newPolyConnects.append(vertOffset + rodPolyConnects[i]);

			if (nRods == 0)
			{
				for (i = 0; i < rodUCoords.length(); i++)
				{
					newUCoords.append(rodUCoords[i]);
					newVCoords.append(rodVCoords[i]);
				}
			}

			for (i = 0; i < rodFvUVIDs.length(); i++)
				newFvUVIDs.append(uvOffset + rodFvUVIDs[i]);
		}

		//ref: https://help.autodesk.com/view/MAYAUL/2018/CHS/?guid=__cpp_ref_class_m_fn_mesh_html
		objTransform = meshFn.create(
			newVerts.length(),
			nNewPolys, 
			newVerts,
			newPolyCounts, 
			newPolyConnects,
			newUCoords, 
			newVCoords,
			MObject::kNullObj, 
			&stat
		);
		/*
		MObject create	(	
			int 	numVertices,
			int 	numPolygons,
			const MFloatPointArray & 	vertexArray,
			const MIntArray & 	polygonCounts,
			const MIntArray & 	polygonConnects,
			const MFloatArray & 	uArray,
			const MFloatArray & 	vArray,
			MObject 	parentOrOwner = MObject::kNullObj,
			MStatus * 	ReturnStatus = NULL 
		)		
		Creates a new polygonal mesh given an array of vertices, polygon connection information, UV information, and sets this function set to operate on the new surface.

		This method is meant to be as efficient as possible and thus assumes that all the given data is topologically correct.

		The parentOrOwner argument is used to specify the owner of the new surface.

		If the parentOrOwner is kMeshData then the created surface will be of type kMeshGeom and will be returned. The parentOrOwner will become the owner of the new mesh.

		If parentOrOwner is NULL then a new transform will be created and returned which will be the parent for the mesh. The new transform will be added to the DAG.

		If parentOrOwner is a DAG node then the new mesh will be returned and the parentOrOwner will become its parent.

		The uv arrays must be of equal size. After using this method to create the mesh and the UV values, you can call assignUVs to assign the corresponding UV ids to the geometry.

		Parameters
		[in]	numVertices	number of vertices
		[in]	numPolygons	number of polygons
		[in]	vertexArray	point (vertex) array. This should include all the vertices in the mesh, and no extras. For example, a cube could have the vertices: { (-1,-1,-1), (1,-1,-1), (1,-1,1), (-1,-1,1), (-1,1,-1), (-1,1,1), (1,1,1), (1,1,-1) }
		[in]	polygonCounts	array of vertex counts for each polygon. For example the cube would have 6 faces, each of which had 4 verts, so the polygonCounts would be {4,4,4,4,4,4}.
		[in]	polygonConnects	array of vertex connections for each polygon. For example, in the cube, we have 4 vertices for every face, so we list the vertices for face0, face1, etc consecutively in the array. These are specified by indexes in the vertexArray: e.g for the cube: { 0, 1, 2, 3, 4, 5, 6, 7, 3, 2, 6, 5, 0, 3, 5, 4,0, 4, 7, 1, 1, 7, 6, 2 }
		[in]	uArray	The array of u values to be set
		[in]	vArray	The array of v values to be set
		[in]	parentOrOwner	parent of the polygon that will be created
		[out]	ReturnStatus	Status code
		Returns
		If parentOrOwner is NULL then the transform for this surface is returned
		If parentOrOwner is a DAG object then the new surface shape is returned
		The surface geometry is returned if parentOrOwner is of type kMeshData
		Status Codes:
		MS::kSuccess The method was successful.
		MS::kLicenseFailure Application not licensed for attempted operation
		MS::kInvalidParameter Array length does not match given item count; parentOrOwner was not valid; or there was no model present to add the object to
		MS::kFailure An object error has occurred.
		MS::kInsufficientMemory Insufficient memory to complete this method
		*/

		if (!stat)
		{
			MGlobal::displayError(MString("Unable to create mesh: ") + stat.errorString());
			return stat;
		}

		objTransforms.append(objTransform);

		meshFn.assignUVs(newPolyCounts, newFvUVIDs);

		meshFn.updateSurface();

		dagFn.setObject(objTransform);
		dagFn.setName("molecule");

		dagMod.commandToExecute(MString("sets -e -fe initialShadingGroup ") + meshFn.name());
	}

	MString cmd("select -r");
	for ( i = 0; i < objTransforms.length(); i++)
	{
		dagFn.setObject(objTransforms[i]);
		cmd += " " + dagFn.name();
	}
	dagMod.commandToExecute(cmd);

	return dagMod.doIt();
}

MStatus Molecule2Cmd::undoIt()
{
	MDGModifier dgMod;
	MFnDagNode dagFn;
	MObject child;

	unsigned int i;
	for (i = 0; i < objTransforms.length(); i++)
	{
		dagFn.setObject(objTransforms[i]);
		child = dagFn.child(0);
		dgMod.deleteNode(child);
		
		dgMod.deleteNode(objTransforms[i]);
	}

	return dgMod.doIt();
}