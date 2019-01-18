// print polygon face info, _twoPolygonMesh.ma
#include <maya/MSimple.h>
#include <maya/MStatus.h>
#include <maya/MArgList.h>
#include <maya/MSelectionList.h>
#include <maya/MItSelectionList.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MGlobal.h>
#include <maya/MDagPath.h>
#include <maya/MObject.h>
#include <maya/MPoint.h>
#include <maya/MString.h>

DeclareSimpleCommand(FaceInfo, "jason.li", "1.0");

MStatus FaceInfo::doIt(const MArgList& args)
{
	MStatus stat = MS::kSuccess;

	MSelectionList selection;
	MGlobal::getActiveSelectionList(selection);

	MDagPath dagPath;
	MObject component;

	int i, polyIndex, polyCount, vertCount;
	MPoint p;
	MString txt;
	
	MItSelectionList iter(selection);
	for (; !iter.isDone(); iter.next())
	{
		iter.getDagPath(dagPath, component);

		MItMeshPolygon polyIter(dagPath, component, &stat);
		if (stat == MS::kSuccess)
		{
			txt += MString("Object: ") + dagPath.fullPathName() + "\n";

			polyCount = polyIter.count();
			txt += MString("# Polygons: ") + polyCount + "\n";

			for (; !polyIter.isDone(); polyIter.next())
			{
				polyIndex = polyIter.index();
				txt += MString("Face ") + polyIndex + "\n";

				vertCount = polyIter.polygonVertexCount();
				txt += MString(" # Verts: ") + vertCount + "\n";

				for (i = 0; i < vertCount; i++)
				{
					p = polyIter.point(i, MSpace::kWorld);
					txt += MString(" (") + p.x + ", " + p.y + ", " + p.z + ")";
				}
				txt += "\n";
			}
		}
	}

	MGlobal::displayInfo(txt);

	return MS::kSuccess;
}