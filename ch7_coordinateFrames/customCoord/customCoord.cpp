// Maya Programming II / Chapter 7 Custom Coordinate Frames

#include <maya/MSimple.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MMatrix.h>
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MQuaternion.h>
#include <maya/MGlobal.h>
#include <maya/MObject.h>
#include <maya/MItSelectionList.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnTransform.h>
#include <maya/MStatus.h>
#include <maya/MArgList.h>

#define _USE_MATH_DEFINES
#include <math.h>

DeclareSimpleCommand(CustomCoord, "jason.li", "1.0");

MStatus CustomCoord::doIt(const MArgList& args)
{
	MSelectionList sel;
	sel.add("es");
	sel.add("obj");

	MDagPath esPath;
	sel.getDagPath(0, esPath);
	MMatrix mEsObjToWorld = esPath.inclusiveMatrix();
	MPoint esPos = MPoint::origin * mEsObjToWorld;

	MDagPath objPath;
	sel.getDagPath(1, objPath);
	MMatrix mObjToWorld = objPath.inclusiveMatrix();
	MPoint objPos = MPoint::origin * mObjToWorld;

	MPoint eyeOrigin(esPos);
	MVector eyeU(objPos - esPos);
	eyeU.normalize();

	MVector eyeV(MVector::yAxis);
	//dot(U, V), if equals 1, U, V will colinear
	if (eyeU * eyeV > 0.999)
	{
		eyeV = MVector::xAxis;
	}

	//W = normalize(cross(U, V))
	MVector eyeW = eyeU ^ eyeV;
	eyeW.normalize();

	//fix V, it must be perpendicular to U
	eyeV = eyeW ^ eyeU;
	// OK, the custom coordinate frames is Done!

	// Using the eye coordinate frame
	// calculate eye coordinate frame
	MQuaternion q;
	MQuaternion qx(MVector::xAxis, eyeU);	// x -> U
	q = qx;

	MVector yRotated = MVector::yAxis.rotateBy(q); // y -> U
	double angle = acos(yRotated * eyeV);
	MQuaternion qy(angle, eyeU);					// y -> V
	if (!eyeV.isEquivalent(yRotated.rotateBy(qy), 1.0e-5))
	{
		angle = 2 * M_PI - angle;
		qy = MQuaternion(angle, eyeU);				// y -> V
	}
	q *= qy;		// concatenated U, V rotation



	MGlobal::getActiveSelectionList(sel);
	MDagPath dagPath;
	MObject component;

	MItSelectionList iter(sel);
	for (; !iter.isDone(); iter.next())
	{
		iter.getDagPath(dagPath, component);
		MFnDagNode dagFn(dagPath);

		MFnTransform transformFn(dagPath);
		transformFn.setRotation(q);
		transformFn.setTranslation(eyeOrigin, MSpace::kTransform);
	}

	// Calculate eye coordinate frame
	/*
	If the three basis vectors of the coordinate  frame are guaranteed to be orthogonal to one
	another  and  have a unit length  (orthanarrnal basis), the vector components  can be used
	to directly set the  rotation  part  (top-left  3  x  3  matrix)  of the  matrix. There  is no  need
	for quaternions. The calculation of the matrix can then be replaced by the following.
	*/
	MMatrix m;
	m(0, 0) = eyeU.x; m(0, 1) = eyeU.y; m(0, 2) = eyeU.z;
	m(1, 0) = eyeV.x; m(1, 1) = eyeV.y; m(1, 2) = eyeV.z;
	m(2, 0) = eyeW.x; m(2, 1) = eyeW.y; m(2, 2) = eyeW.z;
	MTransformationMatrix tm(m);
	tm.setTranslation(eyeOrigin, MSpace::kTransform);

	iter.reset();
	for (; !iter.isDone(); iter.next())
	{
		iter.getDagPath(dagPath, component);
		MFnDagNode dagFn(dagPath);

		MFnTransform transformFn(dagPath);
		//
		transformFn.set(tm);
		//
		transformFn.setRotation(q);
		transformFn.setTranslation(eyeOrigin, MSpace::kTransform);
	}

	return MS::kSuccess;
}