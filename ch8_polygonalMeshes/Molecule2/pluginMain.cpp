#include "molecule2Cmd.h"
#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>

MStatus initializePlugin(MObject obj)
{
	MFnPlugin pluginFn(obj, "jason.li", "1.0");
	MStatus stat;

	stat = pluginFn.registerCommand("molecule2", Molecule2Cmd::creator, Molecule2Cmd::newSyntax);
	if (!stat)
	{
		MGlobal::displayError(MString("registerCommand failed ") + stat.errorString());
	}

	return stat;
}

MStatus uninitializePlugin(MObject obj)
{
	MFnPlugin pluginFn(obj);
	MStatus stat;

	stat = pluginFn.deregisterCommand("molecule2");
	if (!stat)
	{
		MGlobal::displayError(MString("deregisterCommand failed ") + stat.errorString());
	}

	return stat;
}