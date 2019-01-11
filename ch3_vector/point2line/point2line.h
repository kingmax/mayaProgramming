#pragma once
#include <maya/MPxCommand.h>

class Point2Line : MPxCommand
{
public:
	virtual MStatus doIt(const MArgList& args);
	static void *creator();
};

