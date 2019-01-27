#include "moleculeCmd.h"
#include "moleculeNode.h"
#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>

MStatus initializePlugin(MObject obj)
{
	MStatus stat;

	MFnPlugin plugin(obj, "jason.li", "1.0");
	stat = plugin.registerCommand("molecule4",
		MoleculeCmd::creator,
		MoleculeCmd::newSyntax);

	if (!stat)
	{
		MGlobal::displayError(MString("register command failed: ") + stat.errorString());
		return stat;
	}

	stat = plugin.registerNode("molecule4",
		MoleculeNode::id,
		MoleculeNode::creator,
		MoleculeNode::initialize);

	if (!stat)
	{
		MGlobal::displayError(MString("register node failed: ") + stat.errorString());
		return stat;
	}

	stat = plugin.registerUI("molecule4CreateUI", "molecule4DeleteUI");
	if (!stat)
	{
		MGlobal::displayError(MString("register ui failed: ") + stat.errorString());
		return stat;
	}

	return stat;
}

MStatus uninitializePlugin(MObject obj)
{
	MStatus stat;
	MFnPlugin plugin(obj);

	stat = plugin.deregisterCommand("molecule4");
	if (!stat)
	{
		MGlobal::displayError(MString("deregister command failed: ") + stat.errorString());
		return stat;
	}

	stat = plugin.deregisterNode(MoleculeNode::id);
	if (!stat)
	{
		MGlobal::displayError(MString("deregister node failed: ") + stat.errorString());
		return stat;
	}

	return stat;
}