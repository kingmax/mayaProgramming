#include "moleculeNode.h"
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


	}
}

void * MoleculeNode::creator()
{
	return new MoleculeNode;	
	//�������ŵ���Ĭ�Ϲ��캯��,�����κγ�ʼ����Ա����,�����ֶ���ʼ���κγ�Ա��
	//��Ϊ�ಢû����ʽ�����κι��캯�������������Ĭ�Ϲ��캯���Ǻϳɹ��캯����
	//��������ŵ��õĻ�����������������˵���ʼ����ΪĬ��ֵ����int(0).......
	
	//��������ԭ���������ʽ������һ��initialize����������Ա��ʼ��������

	//�������ţ������κγ�ʼ�������Ƿ�����ܿ�һЩ��
}

MStatus MoleculeNode::initialize()
{
	MFnUnitAttribute uAttr;
	MFnNumericAttribute nAttr;
	MFnTypedAttribute tAttr;

	radius = uAttr.create("radius", "rad", MFnUnitAttribute::kDistance, 0.1);
	uAttr.setKeyable(true);	//�������Բ�����ʾ��channelbox,�û��޷����е���
	segments = nAttr.create("segments", "seg", MFnNumericData::kLong, 6);
	nAttr.setKeyable(true);
	ballRatio = nAttr.create("ballRatio", "br", MFnNumericData::kDouble, 2.0);
	nAttr.setKeyable(true);

	inMesh = tAttr.create("inMesh", "im", MFnData::kMesh);
	outMesh = tAttr.create("outMesh", "om", MFnData::kMesh);
	tAttr.setStorable(false); //����compute���ɣ����Բ���Ҫ��

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
