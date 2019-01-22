#include "moleculeCmd.h"
#include <maya/MObject.h>
#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj)
{
	MFnPlugin pluginFn(obj, "jason.li", "1.0");

	MStatus stat;
	stat = pluginFn.registerCommand("molecule1", MoleculeCmd::creator);
	if (!stat)
	{
		stat.perror("registerCommand failed");
	}

	return stat;
}

MStatus uninitializePlugin(MObject obj)
{
	MFnPlugin pluginFn(obj);

	MStatus stat;
	stat = pluginFn.deregisterCommand("molecule1");
	if (!stat)
	{
		stat.perror("deregisterCommand failed");
	}

	return stat;
}