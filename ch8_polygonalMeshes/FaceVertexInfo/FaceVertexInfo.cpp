// print vertex-face info and vertex-color, _twoPolygonMesh.ma

#include <maya/MSimple.h>
#include <maya/MGlobal.h>
#include <maya/MStatus.h>
#include <maya/MArgList.h>
#include <maya/MSelectionList.h>
#include <maya/MItSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MObject.h>
#include <maya/MObject.h>
#include <maya/MColor.h>
#include <maya/MString.h>
#include <maya/MItMeshFaceVertex.h>

DeclareSimpleCommand(FaceVertexInfo, "jason.li", "1.0");

MStatus FaceVertexInfo::doIt(const MArgList& args)
{
	MStatus stat = MS::kSuccess;

	MSelectionList selection;
	MGlobal::getActiveSelectionList(selection);

	MDagPath dagPath;
	MObject component;
	MColor c;
	MString txt;

	MItSelectionList iter(selection);
	for (; !iter.isDone(); iter.next())
	{
		iter.getDagPath(dagPath, component);

		MItMeshFaceVertex fvIter(dagPath, component, &stat);
		if (stat == MS::kSuccess)
		{
			txt += MString("Object: ") + dagPath.fullPathName() + "\n";

			for (; !fvIter.isDone(); fvIter.next())
			{
				int vertID = fvIter.vertId();
				int faceID = fvIter.faceId();
				int faceVertID = fvIter.faceVertId();

				txt += MString(" Face ") + faceID +
					": mesh-relative-vertexID (" + vertID +
					"), face-relative-vertexID(" + faceVertID + ")\n";

				if (fvIter.hasColor())
				{
					fvIter.getColor(c);
					txt += MString(" Color: ") + c.r + ", " + c.g + "," + c.b + "\n";
				}
				else
					txt += MString(" no color\n");
			}
		}
	}

	MGlobal::displayInfo(txt);

	return MS::kSuccess;
}