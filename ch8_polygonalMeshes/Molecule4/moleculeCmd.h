#pragma once

#include <maya/MPxCommand.h>
#include <maya/MDistance.h>
#include <maya/MDagModifier.h>
#include <maya/MObjectArray.h>

class MoleculeCmd : public MPxCommand
{
public:
	virtual MStatus doIt(const MArgList&);
	virtual MStatus redoIt();
	virtual MStatus undoIt();
	virtual bool isUndoable() const { return true; }

	static void *creator() { return new MoleculeCmd; }
	static MSyntax newSyntax();

private:
	MDistance radius;
	int segs;
	double ballRodRatio;

	MDagModifier dagMods[2];
	MObjectArray moleculeNodes;
	MObjectArray meshShapeNodes;
};