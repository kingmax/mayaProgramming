#pragma once

#include <maya/MPxCommand.h>

class MoleculeCmd : public MPxCommand
{
public:
	virtual MStatus doIt(const MArgList&);
	static void *creator() { return new MoleculeCmd(); }
};