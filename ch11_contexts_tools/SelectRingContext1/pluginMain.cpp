#include "selectRingContext1.h"
#include "selectRingContextCmd1.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj)
{
	MFnPlugin pluginFn(obj, "jason.li", "1.0");

	MStatus stat;
	stat = pluginFn.registerContextCommand("selectRingContext1",
		SelectRingContextCmd1::creator);

	if (!stat)
	{
		stat.perror("registerContextCommand failed");
	}

	return stat;
}

MStatus uninitializePlugin(MObject obj)
{
	MFnPlugin pluginFn(obj);

	MStatus stat;
	stat = pluginFn.deregisterContextCommand("selectRingContext1");

	if (!stat)
	{
		stat.perror("deregisterContextCommand failed");
	}

	return stat;
}