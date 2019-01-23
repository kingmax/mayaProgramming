# coding:utf-8
# create a polygon cube using API demo
# OpenMaya.MFnMesh.create(...), https://help.autodesk.com/view/MAYAUL/2018/CHS/?guid=__py_ref_class_open_maya_1_1_m_fn_mesh_html
# C++ API ref: https://help.autodesk.com/view/MAYAUL/2018/CHS/?guid=__cpp_ref_class_m_fn_mesh_html
'''
MObject create	(	
			int 	numVertices,
			int 	numPolygons,
			const MFloatPointArray & 	vertexArray,
			const MIntArray & 	polygonCounts,
			const MIntArray & 	polygonConnects,
			const MFloatArray & 	uArray,
			const MFloatArray & 	vArray,
			MObject 	parentOrOwner = MObject::kNullObj,
			MStatus * 	ReturnStatus = NULL 
		)	
'''

from maya.api import OpenMaya as om

meshFn = om.MFnMesh()
dir(meshFn)
help(meshFn.create)

vPosList = ( om.MPoint(p) for p in ((-1,-1,-1), (1,-1,-1), (1,-1,1), (-1,-1,1), (-1,1,-1), (-1,1,1), (1,1,1), (1,1,-1)) )
'''
# Result: [maya.api.OpenMaya.MPoint(-1, -1, -1, 1),
 maya.api.OpenMaya.MPoint(1, -1, -1, 1),
 maya.api.OpenMaya.MPoint(1, -1, 1, 1),
 maya.api.OpenMaya.MPoint(-1, -1, 1, 1),
 maya.api.OpenMaya.MPoint(-1, 1, -1, 1),
 maya.api.OpenMaya.MPoint(-1, 1, 1, 1),
 maya.api.OpenMaya.MPoint(1, 1, 1, 1),
 maya.api.OpenMaya.MPoint(1, 1, -1, 1)] # 
'''

fCounts = (4,4,4,4,4,4)

# index of vPosList, vertex connections for each face
connectList = (0, 1, 2, 3, 4, 5, 6, 7, 3, 2, 6, 5, 0, 3, 5, 4,0, 4, 7, 1, 1, 7, 6, 2)

uList = None
vList = None
_parent = om.MObject.kNullObj

newObj = meshFn.create(vPosList, fCounts, connectList)
type(newObj)

# 上面创建的Cube物体没有UV, 没有默认材质， 顶点法线是平均的， 跟默认Cube物体有一些差异！！！
