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

	}

}