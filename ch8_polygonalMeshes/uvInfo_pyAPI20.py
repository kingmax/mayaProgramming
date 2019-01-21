# coding:utf-8
# UV info, using Maya Python API 2.0, _TwoPolygonMesh.ma

from maya.api import OpenMaya as om

info = ''

selList = om.MGlobal.getActiveSelectionList()
# dagPath = selList.getDagPath(0)
dagPath, component = selList.getComponent(0)
info += 'Object: %s\n'%(dagPath.fullPathName())

meshFn = om.MFnMesh(dagPath)
# dir(meshFn)
uvSets = meshFn.getUVSetNames()
for name in uvSets:
    info += ' UV Set: %s'%name
    info += ' # UVs: %s\n'%(meshFn.numUVs(name))

# currentUVSet = meshFn.getCurrentUVSetName() 
# Error: AttributeError: file <maya console> line 1: 'OpenMaya.MFnMesh' object has no attribute 'getCurrentUVSetName' # 
from maya import cmds
currentUVSet = cmds.polyUVSet(currentUVSet=True, q=True)[0]
info += ' Current UV Set: %s\n'%currentUVSet

# vIter = om.MItMeshVertex(dagPath)
vIter = om.MItMeshVertex(dagPath, component)
while not vIter.isDone():
    index = vIter.index()
    info += ' Vertex: %s\n'%index
    
    hasUV = False
    
    # uv = vIter.getUV()
    try:
        uv = vIter.getUV(currentUVSet)
        if uv:
            # hasUV = True
            info += ' Vertex UV:%s\n'%uv
    except:
        info += ' No assigned uv\n'
        # break
        
    # fvUs, fvVs, fIDs = vIter.getUVs()
    try:
        fvUs, fvVs, fIDs = vIter.getUVs(currentUVSet)
        # Result: [maya.api.OpenMaya.MFloatArray([0.5, 0.5]), maya.api.OpenMaya.MFloatArray([0.0, 0.0]), maya.api.OpenMaya.MIntArray([0, 1])] # 
        if fvUs:
            hasUV = True
            for i in range(len(fIDs)):
                fIndex = fIDs[i]
                fvIDs = meshFn.getPolygonVertices(fIndex)
                for fvIndex in range(len(fvIDs)):
                    if fvIDs[fvIndex] == index:
                        break
                info += ' Face-vertex UV: face,vertexFace:(%s, %s), UV:(%s, %s)\n'%(fIndex, fvIndex, fvUs[i], fvVs[i])
                
        if not hasUV:
            info += ' No assigned uv\n'
    except:
        pass
        
    vIter.next()

print(info)

'''

Object: |square
 UV Set: map1 # UVs: 6
 UV Set: map2 # UVs: 0
 Current UV Set: map1
 Vertex: 0
 Vertex UV:[0.0, 0.0]
 Face-vertex UV: face,vertexFace:(0, 0), UV:(0.0, 0.0)
 Vertex: 1
 Vertex UV:[0.5, 0.0]
 Face-vertex UV: face,vertexFace:(0, 1), UV:(0.5, 0.0)
 Face-vertex UV: face,vertexFace:(1, 0), UV:(0.5, 0.0)
 Vertex: 2
 Vertex UV:[1.0, 0.0]
 Face-vertex UV: face,vertexFace:(1, 1), UV:(1.0, 0.0)
 Vertex: 3
 Vertex UV:[0.0, 1.0]
 Face-vertex UV: face,vertexFace:(0, 3), UV:(0.0, 1.0)
 Vertex: 4
 Vertex UV:[0.5, 1.0]
 Face-vertex UV: face,vertexFace:(1, 3), UV:(0.5, 1.0)
 Face-vertex UV: face,vertexFace:(0, 2), UV:(0.5, 1.0)
 Vertex: 5
 Vertex UV:[1.0, 1.0]
 Face-vertex UV: face,vertexFace:(1, 2), UV:(1.0, 1.0)

'''

cmds.polyUVSet(uvSet="map2", currentUVSet=True)

