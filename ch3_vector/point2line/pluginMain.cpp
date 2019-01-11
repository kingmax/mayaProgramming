#include "point2line.h"
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj)
{
	MStatus stat;

	MFnPlugin pluginFn(obj, "jason.li", "1.0", "Any");
	stat = pluginFn.registerCommand("point2line", Point2Line::creator);
	if (!stat)
	{
		stat.perror("registerCommand failed");
	}

	return stat;
}

MStatus uninitializePlugin(MObject obj)
{
	MStatus stat;

	MFnPlugin pluginFn(obj, "jason.li", "1.0", "Any");
	stat = pluginFn.deregisterCommand("point2line");
	if (!stat)
	{
		stat.perror("deregisterCommand failed");
	}

	return stat;
}
