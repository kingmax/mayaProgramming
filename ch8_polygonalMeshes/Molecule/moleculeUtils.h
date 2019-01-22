#pragma once

#include <maya/MStatus.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>

int linearIndex(const int r, const int c, const int nRows, const int nCols);

MStatus genBall(const MPoint &center, const double radius, const unsigned int nSegs, int &nPolys, MPointArray &verts, MIntArray &polyCounts, MIntArray &polyConnects);

MStatus genRod(const MPoint &p0, const MPoint &p1, const double radius, const unsigned int nSegs, int &nPolys, MPointArray &verts, MIntArray &polyCounts, MIntArray &polyConnects);