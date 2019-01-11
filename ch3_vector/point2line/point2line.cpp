#include "point2line.h"
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>

MStatus Point2Line::doIt(const MArgList & args)
{
	MPoint p(1.0, 3.0, 4.0);
	// line
	MPoint p0(0, 0, 0);
	MPoint p1(1, 0, 0);

	MVector a = p - p0;
	MVector b = p1 - p0;
	b.normalize();

	MVector c = (a * b) * b;
	MVector d = a - c;
	double dist = d.length();
	MGlobal::displayInfo(MString("distance: ") + dist);

	return MS::kSuccess;
}

void * Point2Line::creator()
{
	return new Point2Line();
}
