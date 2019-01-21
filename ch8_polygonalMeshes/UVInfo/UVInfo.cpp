// print UV info, _twoPolygonMesh.ma

#include <maya/MSimple.h>

#include <maya/MStatus.h>
#include <maya/MGlobal.h>
#include <maya/MArgList.h>
#include <maya/MDagPath.h>
#include <maya/MObject.h>
#include <maya/MItSelectionList.h>
#include <maya/MString.h>
#include <maya/MFnMesh.h>
#include <maya/MItMeshVertex.h>
#include <maya/MFloatArray.h>
#include <maya/MIntArray.h>

DeclareSimpleCommand(UVInfo, "jason.li", "1.0");

MStatus UVInfo::doIt(const MArgList& args)
{
	MStatus stat = MS::kSuccess;

	MSelectionList selection;
	MGlobal::getActiveSelectionList(selection);

	MDagPath dagPath;
	MObject component;
	unsigned int i;
	int fIndex, vIndex;
	MString txt;

	MItSelectionList iter(selection);
	for (; !iter.isDone(); iter.next())
	{
		iter.getDagPath(dagPath, component);

		MFnMesh meshFn(dagPath, &stat);
		if (!stat)
		{
			continue;
		}

		txt += MString("Object: ") + dagPath.fullPathName() + "\n";
		
		MStringArray uvSetNames;
		meshFn.getUVSetNames(uvSetNames);
		for ( i = 0; i < uvSetNames.length(); i++)
		{
			txt += MString(" UV Set: ") + uvSetNames[i];
			txt += MString(" # UVs: ") + meshFn.numUVs(uvSetNames[i]) + "\n";
		}

		MString cUVSetName;
		meshFn.getCurrentUVSetName(cUVSetName);
		txt += MString(" Current UV Set: ") + cUVSetName + "\n";

		MItMeshVertex vertIter(dagPath, component, &stat);
		if (!stat)
		{
			continue;
		}

		float2 vUV;
		MFloatArray fvUs;
		MFloatArray fvVs;
		MIntArray faceIds;
		MIntArray vertIds;
		unsigned int fvIndex;

		for (; !vertIter.isDone(); vertIter.next())
		{
			vIndex = vertIter.index();
			txt += MString(" Vertex: ") + vIndex + "\n";

			bool hasUV = false;

			stat = vertIter.getUV(vUV, &cUVSetName);
			if (stat)
			{
				txt += MString(" Vertex UV: (") + vUV[0] + ", " + vUV[1] + ")\n";
				hasUV = true;
			}

			stat = vertIter.getUVs(fvUs, fvVs, faceIds, &cUVSetName);
			if (stat)
			{
				for ( i = 0; i < faceIds.length(); i++)
				{
					fIndex = faceIds[i];

					meshFn.getPolygonVertices(fIndex, vertIds);
					for ( fvIndex = 0; fvIndex < vertIds.length(); fvIndex++)
					{
						if (vertIds[fvIndex] == vIndex)
						{
							break;
						}
					}

					txt += MString(" Face-Vertex UV: face, vertex: (") + fIndex + ", " + fvIndex + ") uv:(" + fvUs[i] + ", " + fvVs[i] + ")\n";
				}
				hasUV = true;
			}

			if (!hasUV)
			{
				txt += " No assigned uv\n";
			}
		}
	}

	MGlobal::displayInfo(txt);

	return MS::kSuccess;
}