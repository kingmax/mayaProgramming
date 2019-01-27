#include "moleculeNode.h"
#include "util.h"
#include <maya/MFnUnitAttribute.h>
#include <maya/MDistance.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MDataHandle.h>
#include <maya/MFnMesh.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MFnMeshData.h>
#include <maya/MItMeshEdge.h>
#include <maya/MGlobal.h>


MTypeId MoleculeNode::id(0x00337);
MObject MoleculeNode::radius;
MObject MoleculeNode::segments;
MObject MoleculeNode::ballRatio;
MObject MoleculeNode::inMesh;
MObject MoleculeNode::outMesh;


MStatus MoleculeNode::computer(const MPlug & plug, MDataBlock & data)
{
	MStatus stat;

	MDataHandle stateHnd = data.inputValue(state);
	int state = stateHnd.asInt();
	if (state == 1)
	{
		MDataHandle inMeshHnd = data.inputValue(inMesh);
		MDataHandle outMeshHnd = data.outputValue(outMesh);
		outMeshHnd.set(inMeshHnd.asMesh());
		data.setClean(plug);
		return MS::kSuccess;
	}

	if (plug == outMesh)
	{
		MDataHandle radiusHnd = data.inputValue(radius);
		MDataHandle segmentsHnd = data.inputValue(segments);
		MDataHandle ballRatioHnd = data.inputValue(ballRatio);
		MDataHandle inMeshHnd = data.inputValue(inMesh);
		MDataHandle outMeshHnd = data.outputValue(outMesh);

		double radius = radiusHnd.asDouble();
		int segs = segmentsHnd.asInt();
		double ballRatio = ballRatioHnd.asDouble();

		MObject inMeshObj = inMeshHnd.asMeshTransformed();
		MFnMesh inMeshFn(inMeshObj);

		MFnMeshData meshDataFn;
		MObject newMeshData = meshDataFn.create();

		int nBallPolys;
		MPointArray ballVerts;
		MIntArray ballPolyCounts;
		MIntArray ballPolyConnects;
		MFloatArray ballUCoords;
		MFloatArray ballVCoords;
		MIntArray ballFvUVIDs;

		genBall(MPoint::origin, ballRatio * radius, segs, nBallPolys,
			ballVerts, ballPolyCounts, ballPolyConnects,
			true, ballUCoords, ballVCoords, ballFvUVIDs);

		unsigned int i, j, vertOffset;
		MPointArray meshVerts;
		MPoint p0, p1;

		int nRodPolys;
		MPointArray rodVerts;
		MIntArray rodPolyCounts;
		MIntArray rodPolyConnects;
		MFloatArray rodUCoords;
		MFloatArray rodVCoords;
		MIntArray rodFvUVIDs;

		int nNewPolys;
		MPointArray newVerts;
		MIntArray newPolyCounts;
		MIntArray newPolyConnects;
		MFloatArray newUCoords;
		MFloatArray newVCoords;
		MIntArray newFvUVIDs;

		int uvOffset;

		uvOffset = 0;
		nNewPolys = 0;
		newVerts.clear();
		newPolyCounts.clear();
		newPolyConnects.clear();
		newUCoords.clear();
		newVCoords.clear();
		newFvUVIDs.clear();

		inMeshFn.getPoints(meshVerts, MSpace::kWorld);
		for ( i = 0; i < meshVerts.length(); i++)
		{
			vertOffset = newVerts.length();
			nNewPolys += nBallPolys;

			for (j = 0; j < ballVerts.length(); j++)
			{
				newVerts.append(meshVerts[i] + ballVerts[j]);
			}
			for (j = 0; j < ballPolyCounts.length(); j++)
			{
				newPolyCounts.append(ballPolyCounts[j]);
			}
			for (j = 0; j < ballPolyConnects.length(); j++)
			{
				newPolyConnects.append(vertOffset + ballPolyConnects[j]);
			}

			if (i == 0)
			{
				for (j = 0; j < ballUCoords.length(); j++)
				{
					newUCoords.append(ballUCoords[j]);
					newVCoords.append(ballVCoords[j]);
				}
			}

			for ( j = 0; j < ballFvUVIDs.length(); j++)
			{
				newFvUVIDs.append(uvOffset + ballFvUVIDs[j]);
			}
		}

		uvOffset = newUCoords.length();

		int nRods = 0;
		MItMeshEdge edgeIter(inMeshObj);
		for (; !edgeIter.isDone(); edgeIter.next(), nRods++)
		{
			p0 = edgeIter.point(0, MSpace::kWorld);
			p1 = edgeIter.point(1, MSpace::kWorld);

			genRod(p0, p1,
				radius, segs, nRodPolys,
				rodVerts, rodPolyCounts, rodPolyConnects,
				nRods == 0, rodUCoords, rodVCoords,
				rodFvUVIDs);

			vertOffset = newVerts.length();
			nNewPolys += nRodPolys;

			for ( i = 0; i < rodVerts.length(); i++)
			{
				newVerts.append(rodVerts[i]);
			}
			for ( i = 0; i < rodPolyCounts.length(); i++)
			{
				newPolyCounts.append(rodPolyCounts[i]);
			}
			for ( i = 0; i < rodPolyConnects.length(); i++)
			{
				newPolyConnects.append(vertOffset + rodPolyConnects[i]);
			}

			if (nRods == 0)
			{
				for ( i = 0; i < rodUCoords.length(); i++)
				{
					newUCoords.append(rodUCoords[i]);
					newVCoords.append(rodVCoords[i]);
				}
			}

			for ( i = 0; i < rodFvUVIDs.length(); i++)
			{
				newFvUVIDs.append(uvOffset + rodFvUVIDs[i]);
			}
		}

		MFnMesh meshFn;
		meshFn.create(newVerts.length(), nNewPolys, newVerts,
			newPolyCounts, newPolyConnects,
			newUCoords, newVCoords,
			newMeshData, &stat);

		if (!stat)
		{
			MGlobal::displayError(MString("Unable to create mesh: ") + stat.errorString());
			return stat;
		}

		meshFn.assignUVs(newPolyCounts, newFvUVIDs);
		meshFn.updateSurface();

		outMeshHnd.set(newMeshData);
		data.setClean(plug);
	}
	else
	{
		stat = MS::kUnknownParameter;
	}

	return stat;
}

void * MoleculeNode::creator()
{
	return new MoleculeNode;	
	//不加括号调节默认构造函数,不作任何初始化成员操作,必须手动初始化任何成员！
	//因为类并没有显式定义任何构造函数，所以这里的默认构造函数是合成构造函数。
	//如果加括号调用的话，对于内置类型来说会初始化其为默认值，如int(0).......
	
	//大概是这个原因，这个类显式定义了一个initialize函数来做成员初始化操作？

	//不加括号，不做任何初始化操作是否对性能快一些？
}

MStatus MoleculeNode::initialize()
{
	MFnUnitAttribute uAttr;
	MFnNumericAttribute nAttr;
	MFnTypedAttribute tAttr;

	radius = uAttr.create("radius", "rad", MFnUnitAttribute::kDistance, 0.1);
	uAttr.setKeyable(true);	//否则属性不会显示在channelbox,用户无法进行调整
	segments = nAttr.create("segments", "seg", MFnNumericData::kLong, 6);
	nAttr.setKeyable(true);
	ballRatio = nAttr.create("ballRatio", "br", MFnNumericData::kDouble, 2.0);
	nAttr.setKeyable(true);

	inMesh = tAttr.create("inMesh", "im", MFnData::kMesh);
	outMesh = tAttr.create("outMesh", "om", MFnData::kMesh);
	tAttr.setStorable(false); //依赖compute生成，所以不需要存

	addAttribute(radius);
	addAttribute(segments);
	addAttribute(ballRatio);
	addAttribute(inMesh);
	addAttribute(outMesh);

	attributeAffects(radius, outMesh);
	attributeAffects(segments, outMesh);
	attributeAffects(ballRatio, outMesh);
	attributeAffects(inMesh, outMesh);

	return MS::kSuccess;
}

MDistance MoleculeNode::radiusDefault()
{
	MFnUnitAttribute uAttr(radius);
	MDistance d;
	uAttr.getDefault(d);
	return d;
}

int MoleculeNode::segmentsDefault()
{
	MFnNumericAttribute nAttr(segments);
	int d;
	nAttr.getDefault(d);
	return d;
}

double MoleculeNode::ballRatioDefault()
{
	MFnNumericAttribute nAttr(ballRatio);
	double d;
	nAttr.getDefault(d);
	return d;
}
