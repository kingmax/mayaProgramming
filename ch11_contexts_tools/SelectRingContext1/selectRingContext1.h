#pragma once
#include <maya/MStatus.h>
#include <maya/MPxContext.h>
#include <maya/MEvent.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionMask.h>
#include <maya/MString.h>

class SelectRingContext1 : public MPxContext
{
public:
	SelectRingContext1();

	virtual void toolOnSetup(MEvent &event);
	virtual void toolOffCleanup();

	virtual MStatus doPress(MEvent &event);
	virtual MStatus doRelease(MEvent &event);

private:
	MGlobal::MSelectionMode prevSelMode;
	MSelectionMask prevCompMask;
	MSelectionMask prevObjMask;

	MGlobal::ListAdjustment listAdjust;

	short pressX, pressY;
	short releaseX, releaseY;
	int clickBoxSize;

	static const MString helpText;
};