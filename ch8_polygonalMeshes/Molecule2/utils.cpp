#include "utils.h"
#include <maya/MStatus.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#define _USE_MATH_DEFINES
#include <math.h>

int linearIndex(const int r, const int c, const int nRows, const int nCols)
{
	return (r % nRows) * nCols + (c % nCols);
}


MStatus genBall(
	const MPoint &center,
	const double radius,
	const unsigned int nSegs,

	int &nPolys,
	MPointArray &verts,
	MIntArray &polyCounts,
	MIntArray &polyConnects,

	const bool genUVs,
	MFloatArray &uCoords,
	MFloatArray &vCoords,
	MIntArray &fvUVIDs
)
{
	verts.clear();
	polyCounts.clear();
	polyConnects.clear();

	if (genUVs)
	{
		uCoords.clear();
		vCoords.clear();
		fvUVIDs.clear();
	}

	int nAzimuthSegs = nSegs * 2; // ����2���ֶ� (ˮƽԲ���з�)
	int nZenithSegs = nSegs;	  // γ��		 (��ֱԲ���з�)
	int nAzimuthPts = nAzimuthSegs;
	int nZenithPts = nZenithSegs + 1;

	double azimIncr = 2.0 * M_PI / nAzimuthSegs;
	double zeniIncr = M_PI / nZenithSegs;

	MPoint p;
	double azimuth, zenith;
	double sinZenith;
	int azi, zeni;

	// ������Ķ�������
	for ( zeni = 0, zenith = 0.0; zeni < nZenithPts; zeni++, zenith += zeniIncr)
	{
		for ( azi = 0, azimuth=0.0; azi < nAzimuthPts; azi++, azimuth += azimIncr)
		{
			sinZenith = sin(zenith);
			p.x = radius * sinZenith * cos(azimuth);
			p.y = radius * cos(zenith);
			p.z = radius * sinZenith * sin(azimuth);

			verts.append(p);
		}
	}

	int nUCols = nAzimuthSegs + 1;
	int nVRows = nZenithSegs + 1;
	// ����UV����
	if (genUVs)
	{
		int nUVCoords = nUCols * nVRows; // UV�������
		uCoords.setLength(nUVCoords);
		uCoords.clear();
		vCoords.setLength(nUVCoords);
		vCoords.clear();

		float uIncr = 1.0f / nAzimuthSegs;
		float vIncr = 1.0f / nZenithSegs;
		float u, v;
		int ui, vi;

		for (vi = 0, v = 0.0; vi < nVRows; vi++, v += vIncr)
		{
			for (ui = 0, u = 0.0; ui < nUCols; ui++, u += uIncr)
			{
				uCoords.append(u);
				vCoords.append(v);
			}
		}
	}

	nPolys = nAzimuthSegs * nZenithSegs;

	polyCounts.setLength(nPolys);
	int i;
	// ���������涼��4��������ɣ�ʵ�����ڶ������ǲ�����ģ��ж������ѻ���һ�������
	for (i = 0; i < nPolys; i++)
		polyCounts[i] = 4;

	// ��Ƕ������ӹ�ϵ �� �涥��UV ID ��ע�⣺ֻ�Ǳ�Ƕ���λ�����������е�����������ʵ�ʹ���Meshʱ���ң���
	for ( zeni = 0; zeni < nZenithSegs; zeni++)
	{
		for ( azi = 0; azi < nAzimuthSegs; azi++)
		{
			polyConnects.append(linearIndex(zeni, azi, nZenithPts, nAzimuthPts));
			polyConnects.append(linearIndex(zeni, azi+1, nZenithPts, nAzimuthPts));
			polyConnects.append(linearIndex(zeni+1, azi+1, nZenithPts, nAzimuthPts));
			polyConnects.append(linearIndex(zeni+1, azi, nZenithPts, nAzimuthPts));

			if (genUVs)
			{
				fvUVIDs.append(linearIndex(zeni, azi, nVRows, nUCols));
				fvUVIDs.append(linearIndex(zeni, azi+1, nVRows, nUCols));
				fvUVIDs.append(linearIndex(zeni+1, azi+1, nVRows, nUCols));
				fvUVIDs.append(linearIndex(zeni+1, azi, nVRows, nUCols));
			}
		}
	}

	return MS::kSuccess;
}


MStatus genRod(
	const MPoint &p0,
	const MPoint &p1,
	const double radius,
	const unsigned int nSegs,

	int &nPolys,
	MPointArray &verts,
	MIntArray &polyCounts,
	MIntArray &polyConnects,

	const bool genUVs,
	MFloatArray &uCoords,
	MFloatArray &vCoords,
	MIntArray &fvUVIDs
)
{
	verts.clear();
	polyCounts.clear();
	polyConnects.clear();
	if (genUVs)
	{
		uCoords.clear();
		vCoords.clear();
		fvUVIDs.clear();
	}

	unsigned int nCirclePts = nSegs;
	unsigned int nVerts = 2 * nCirclePts;

	// ����һ���ֲ�����ϵ
	MVector vec(p1 - p0);
	MVector up(0.0, 1.0, 0.0); // ������
	MVector xAxis, yAxis, zAxis;
	yAxis = vec.normal();	// ȷ�� Y ��
	if (up.isParallel(yAxis, 0.1))
	{
		// ���Y��������ӽ�ͬһ������ı�������Ķ��� ����֮ǰ��ֱ��
		up = MVector(1.0, 0.0, 0.0);
	}
	xAxis = yAxis ^ up;		//ͨ���������X��
	zAxis = (xAxis ^ yAxis).normal(); //����Z��
	xAxis = (yAxis ^ zAxis).normal(); //����X��, ���Y��������֮�䲻��90�ȴ�ֱ��ϵ�Ļ�����Ҫ����

	verts.setLength(nVerts);
	double angleIncr = 2.0 * M_PI / nSegs;
	double angle;
	MPoint p;
	double x, z;
	unsigned int i;
	for ( i = 0, angle = 0.0; i < nCirclePts; i++, angle += angleIncr)
	{
		x = radius * cos(angle); //cos <-> x / r
		z = radius * sin(angle); //sin <-> y / r, ��ΪY�ᶨ��Ϊ���ƽ�з�����������Ҫʹ��X, Z��

		p = p0 + x * xAxis + z * zAxis; //�����ӷ�, ����ԭ�� p0 ��> ��X��ǰ�� ��> ��Z��ǰ�� ����Ŀ��λ��
		verts[i] = p;
		p += vec;
		verts[i + nCirclePts] = p; //???
	}

	int nUCols = nSegs + 1;
	int nVRows = 2;
	if (genUVs)
	{
		int nUVCoords = nUCols * nVRows;
		uCoords.setLength(nUVCoords);
		uCoords.clear();
		vCoords.setLength(nUVCoords);
		vCoords.clear();

		float uIncr = 1.0f / nSegs;
		float u, v;
		int ui, vi;
		for ( vi = 0, v=0.0; vi < nVRows; vi++, v+=1.0)
		{
			for ( ui = 0, u=0.0; ui < nUCols; ui++, u+=uIncr)
			{
				uCoords.append(u);
				vCoords.append(v);
			}
		}
	}

	nPolys = nSegs;

	polyCounts.setLength(nPolys);
	for ( i = 0; i < polyCounts.length(); i++)
	{
		polyCounts[i] = 4;
	}

	polyConnects.setLength(nPolys * 4);
	polyConnects.clear();
	for ( i = 0; i < nSegs; i++)
	{
		polyConnects.append(linearIndex(0, i, 2, nCirclePts));
		polyConnects.append(linearIndex(0, i+1, 2, nCirclePts));
		polyConnects.append(linearIndex(1, i+1, 2, nCirclePts));
		polyConnects.append(linearIndex(1, i, 2, nCirclePts));

		if (genUVs)
		{
			fvUVIDs.append(linearIndex(0, i, nVRows, nUCols));
			fvUVIDs.append(linearIndex(0, i+1, nVRows, nUCols));
			fvUVIDs.append(linearIndex(1, i+1, nVRows, nUCols));
			fvUVIDs.append(linearIndex(1, i, nVRows, nUCols));
		}
	}

	return MS::kSuccess;
}