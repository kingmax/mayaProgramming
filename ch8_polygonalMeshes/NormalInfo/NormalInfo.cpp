#include <maya/MSimple.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MItSelectionList.h>
#include <maya/MStatus.h>
#include <maya/MString.h>
#include <maya/MArgList.h>
#include <maya/MVector.h>
#include <maya/MDagPath.h>
#include <maya/MObject.h>
#include <maya/MFnMesh.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MItMeshVertex.h>
#include <maya/MIntArray.h>

void addData(
	MString &txt,
	const int fIndex,
	const int vIndex,
	const int fvIndex,
	const MVector &fNormal,
	const MVector &vNormal,
	const MVector &fvNormal
)
{
	txt += MString(" Face: ") + fIndex + " Vertex: " + vIndex + " Face-Vertex: " + fvIndex + "\n";
	txt += MString(" Face Normal: (") + fNormal.x + ", " + fNormal.y + ", " + fNormal.z + ")\n";
	txt += MString(" VertexNormal:(") + vNormal.x + ", " + vNormal.y + ", " + vNormal.z + ")\n";
	txt += MString(" Face-VertexNormal:(") + fvNormal.x + ", " + fvNormal.y + ", " + fvNormal.z + ")\n";
}

DeclareSimpleCommand(NormalInfo, "jason.li", "1.0");

MStatus NormalInfo::doIt(const MArgList& args)
{
	MStatus stat = MS::kSuccess;
	
	MSelectionList selection;
	MGlobal::getActiveSelectionList(selection);

	MDagPath dagPath;
	MObject component;
	unsigned int i, nVerts;
	int fIndex, vIndex, fvIndex;
	MVector fNormal, vNormal, fvNormal;
	MString txt;

	MItSelectionList iter(selection);
	for (; !iter.isDone(); iter.next())
	{
		iter.getDagPath(dagPath, component);

		MFnMesh meshFn(dagPath);

		MItMeshPolygon faceIter(dagPath, component, &stat);
		if (stat == MS::kSuccess)
		{
			txt += MString("Object: ") + dagPath.fullPathName() + "\n";

			for (; !faceIter.isDone(); faceIter.next())
			{
				nVerts = faceIter.polygonVertexCount();

				for (i = 0; i < nVerts; i++)
				{
					fvIndex = i;
					fIndex = faceIter.index();
					vIndex = faceIter.vertexIndex(i);

					faceIter.getNormal(fNormal);
					meshFn.getVertexNormal(vIndex, vNormal);
					faceIter.getNormal(fvIndex, fvNormal);

					addData(txt, fIndex, vIndex, fvIndex, fNormal, vNormal, fvNormal);
				}
			}
		}
		else
		{
			MItMeshVertex vertIter(dagPath, component, &stat);

			if (stat == MS::kSuccess)
			{
				txt = MString("Object: ") + dagPath.fullPathName() + "\n";

				MIntArray faceIDs, vertIDs;

				for (; !vertIter.isDone(); vertIter.next())
				{
					vIndex = vertIter.index();

					vertIter.getNormal(vNormal);
					vertIter.getConnectedFaces(faceIDs);

					for ( i = 0;  i < faceIDs.length();  i++)
					{
						fIndex = faceIDs[i];

						meshFn.getPolygonNormal(fIndex, fNormal);
						meshFn.getFaceVertexNormal(fIndex, vIndex, fvNormal);

						meshFn.getPolygonVertices(fIndex, vertIDs);
						for (fvIndex = 0; fvIndex < int(vertIDs.length()); fvIndex++)
						{
							if ( vertIDs[fvIndex] == vIndex )
							{
								break;
							}
						}
						addData(txt, fIndex, vIndex, fvIndex, fNormal, vNormal, fvNormal);
					}
				}

			}
		}

	}
	MGlobal::displayInfo(txt);

	return MS::kSuccess;
}