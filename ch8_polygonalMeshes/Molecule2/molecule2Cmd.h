#pragma once
#include <maya/MDistance.h>
#include <maya/MPxCommand.h>
#include <maya/MDagPathArray.h>
#include <maya/MObjectArray.h>

class Molecule2Cmd : public MPxCommand
{
public:
	virtual MStatus doIt(const MArgList&);
	virtual MStatus redoIt();
	virtual MStatus undoIt();
	virtual bool isUndoable() const;

	static void *creator();
	static MSyntax newSyntax();

private:
	MDistance radius;
	int segs;
	double ballRodRatio;
	MDagPathArray selMeshes;
	MObjectArray objTransforms;
};


