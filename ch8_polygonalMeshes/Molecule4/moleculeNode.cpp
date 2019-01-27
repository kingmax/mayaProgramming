#include "moleculeNode.h"

MTypeId MoleculeNode::id(0x00337);
MObject MoleculeNode::radius;
MObject MoleculeNode::segments;
MObject MoleculeNode::ballRatio;
MObject MoleculeNode::inMesh;
MObject MoleculeNode::outMesh;


MStatus MoleculeNode::computer(const MPlug & plug, MDataBlock & data)
{
	return MStatus();
}

void * MoleculeNode::creator()
{
	return nullptr;
}

MStatus MoleculeNode::initialize()
{
	return MStatus();
}

MDistance MoleculeNode::radiusDefault()
{
	return MDistance();
}

int MoleculeNode::segmentsDefault()
{
	return 0;
}

double MoleculeNode::ballRatioDefault()
{
	return 0.0;
}
