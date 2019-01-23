#pragma once

MStatus genBall(
	const MPoint &center,
	const double radius,
	const unsigned int nSegs,

	int &nPolys, 
	MPointArray &verts, 
	MIntArray &polyCounts,
	MIntArray &polyConnects,
	
	const bool genUVs,
	MFloatArray &uCoords,
	MFloatArray &vCoords,
	MIntArray &fvUVIDs
	);

MStatus genRod(
	const MPoint &p0,
	const MPoint &p1,
	const double radius,
	const unsigned int nSegs,

	int &nPolys,
	MPointArray &verts,
	MIntArray &polyCounts,
	MIntArray &polyConnects,

	const bool genUVs,
	MFloatArray &uCoords,
	MFloatArray &vCoords,
	MIntArray &fvUVIDs
);
