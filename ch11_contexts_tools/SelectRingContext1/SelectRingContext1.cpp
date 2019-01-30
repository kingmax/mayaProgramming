#include "selectRingContext1.h"

#include <maya/MPxContext.h>
#include <maya/MGlobal.h>
#include <maya/MStatus.h>
#include <maya/MSelectionMask.h>
#include <maya/MEvent.h>
#include <maya/MString.h>
#include <maya/MCursor.h>
#include <maya/MSelectionList.h>
#include <maya/MObject.h>
#include <maya/MDagPath.h>
#include <maya/MFn.h>
#include <maya/MItSelectionList.h>
#include <maya/MItMeshEdge.h>
#include <maya/MIntArray.h>
#include <maya/MFnSingleIndexedComponent.h>
#include <maya/MItMeshPolygon.h>

const MString SelectRingContext1::helpText("Click on an edge");

SelectRingContext1::SelectRingContext1()
{
	setTitleString("Select Ring Tool");
}

void SelectRingContext1::toolOnSetup(MEvent &event)
{
	MGlobal::executeCommand("selectPref -query -clickBoxSize", clickBoxSize);
	setHelpString(helpText);
	setCursor(MCursor::editCursor);

	prevSelMode = MGlobal::selectionMode();
	if (prevSelMode == MGlobal::kSelectComponentMode)
	{
		prevCompMask = MGlobal::componentSelectionMask();
	}
	else
	{
		prevObjMask = MGlobal::objectSelectionMask();
	}
}

void SelectRingContext1::toolOffCleanup()
{
	MGlobal::setSelectionMode(prevSelMode);
	if (prevSelMode == MGlobal::kSelectComponentMode)
	{
		MGlobal::setComponentSelectionMask(prevCompMask);
	}
	else
	{
		MGlobal::setObjectSelectionMask(prevObjMask);
	}
}

MStatus SelectRingContext1::doPress(MEvent &event)
{
	listAdjust = MGlobal::kReplaceList;
	if (event.isModifierShift() || event.isModifierControl())
	{
		if (event.isModifierShift())
		{
			if (event.isModifierControl())
			{
				listAdjust = MGlobal::kAddToList;
			}
			else
			{
				listAdjust = MGlobal::kXORWithList;
			}
		}
		else
		{
			if (event.isModifierControl())
			{
				listAdjust = MGlobal::kRemoveFromList;
			}
		}
	}

	event.getPosition(pressX, pressY);
	return MS::kSuccess;
}

MStatus SelectRingContext1::doRelease(MEvent &event)
{
	event.getPosition(releaseX, releaseY);
	if (abs(pressX - releaseX) > 1 || abs(pressY - releaseY) > 1)
	{
		MGlobal::displayWarning("Click on a single edge");
		return MS::kFailure;
	}

	int halfClickBoxSize = clickBoxSize / 2;
	pressX -= halfClickBoxSize;
	pressY -= halfClickBoxSize;
	releaseX = pressX + clickBoxSize;
	releaseY = pressY + clickBoxSize;

	MSelectionList curSel;
	MGlobal::getActiveSelectionList(curSel);

	MGlobal::setSelectionMode(MGlobal::kSelectObjectMode);
	MGlobal::setComponentSelectionMask(MSelectionMask(MSelectionMask::kSelectObjectsMask));
	MGlobal::selectFromScreen(pressX, pressY, releaseX, releaseY, MGlobal::kReplaceList);
	MGlobal::executeCommand("hilite");

	MGlobal::setSelectionMode(MGlobal::kSelectComponentMode);
	MGlobal::setComponentSelectionMask(MSelectionMask(MSelectionMask::kSelectMeshEdges));
	MGlobal::selectFromScreen(pressX, pressY, releaseX, releaseY, MGlobal::kReplaceList);

	MSelectionList origEdgesSel;
	MGlobal::getActiveSelectionList(origEdgesSel);
	MSelectionList newEdgesSel;
	MDagPath dagPath;
	MObject component;

	MItSelectionList selIter(origEdgesSel, MFn::kMeshEdgeComponent);
	if (!selIter.isDone())
	{
		selIter.getDagPath(dagPath, component);

		MIntArray faces;
		MItMeshEdge edgeIter(dagPath, component);

		MIntArray edgesVisited, facesVisited;
		int edgeIndex, faceIndex;
		int prevIndex;
		unsigned int i;
		bool finished = false;
		while (!finished)
		{
			edgeIndex = edgeIter.index();
			edgesVisited.append(edgeIndex);

			MFnSingleIndexedComponent indexedCompFn;
			MObject newComponent = indexedCompFn.create(MFn::kMeshEdgeComponent);
			indexedCompFn.addElement(edgeIndex);
			newEdgesSel.add(dagPath, newComponent);
			edgeIter.getConnectedFaces(faces);
			faceIndex = faces[0];
			if (faces.length() > 1)
			{
				for ( i = 0; i < facesVisited.length(); i++)
				{
					if (faceIndex == facesVisited[i])
					{
						faceIndex = faces[1];
						break;
					}
				}
			}

			facesVisited.append(faceIndex);
			MItMeshPolygon polyIter(dagPath);
			polyIter.setIndex(faceIndex, prevIndex);

			MIntArray edges;
			polyIter.getEdges(edges);

			unsigned int edgeFaceIndex = 0;
			for ( i = 0; i < edges.length(); i++)
			{
				if (edges[i] == edgeIter.index())
				{
					edgeFaceIndex = i;
					break;
				}
			}

			edgeIndex = edges[(edgeFaceIndex + (edges.length() / 2)) % edges.length()];
			edgeIter.setIndex(edgeIndex, prevIndex);

			for ( i = 0; i < edgesVisited.length(); i++)
			{
				if (edgeIndex == edgesVisited[i])
				{
					finished = true;
					break;
				}
			}
		}
	}

	MGlobal::setActiveSelectionList(curSel, MGlobal::kRemoveFromList);
	MGlobal::selectCommand(newEdgesSel, listAdjust);

	return MS::kSuccess;
}