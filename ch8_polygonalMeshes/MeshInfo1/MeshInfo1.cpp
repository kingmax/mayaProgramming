#include <maya/MSimple.h>
#include <maya/MStatus.h>
#include <maya/MArgList.h>
#include <maya/MSelectionList.h>
#include <maya/MItSelectionList.h>
#include <maya/MGlobal.h>
#include <maya/MDagPath.h>
#include <maya/MObject.h>
#include <maya/MString.h>
#include <maya/MItMeshVertex.h>
#include <maya/MPoint.h>

DeclareSimpleCommand(MeshInfo1, "jason.li", "1.0");

MStatus MeshInfo1::doIt(const MArgList& args)
{
	MStatus stat = MS::kSuccess;

	MSelectionList selection;
	MGlobal::getActiveSelectionList(selection);

	MDagPath dagPath;
	MObject component;
	int vertCount, vertIndex;
	MString txt;
	MItSelectionList iter(selection);
	for (; !iter.isDone(); iter.next())
	{
		iter.getDagPath(dagPath, component);
		MItMeshVertex meshIter(dagPath, component, &stat);
		if (stat == MS::kSuccess)
		{
			txt += dagPath.fullPathName() + "\n";

			vertCount = meshIter.count();
			txt += MString("# Vertices: ") + vertCount + "\n";

			for (; !meshIter.isDone(); meshIter.next())
			{
				MPoint pt = meshIter.position(MSpace::kWorld);
				vertIndex = meshIter.index();
				txt += MString(" ") + vertIndex + ": " + pt.x + ", " + pt.y + ", " + pt.z + "\n";
			}
		}
	}

	MGlobal::displayInfo(txt);

	return MS::kSuccess;
}