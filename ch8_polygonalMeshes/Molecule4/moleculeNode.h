#pragma once
#include <maya/MPxNode.h>

class MoleculeNode : public MPxNode
{
public:
	virtual MStatus computer(const MPlug &plug, MDataBlock &data);
	static void *creator();
	static MStatus initialize();

	static MObject radius;
	static MObject segments;
	static MObject ballRatio;
	static MObject inMesh;
	static MObject outMesh;

	static MTypeId id;

	static MDistance radiusDefault();
	static int segmentsDefault();
	static double ballRatioDefault();
};