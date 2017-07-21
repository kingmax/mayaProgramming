#coding:utf-8
#queryNormalInfo.py

import maya.cmds as cmds;
import maya.mel as mel;

def make_scene():
    cmds.file(new=True, f=True)
    cmds.polyCube(name='cube')
    cmds.polyOptions(displayNormal=True)
    mel.eval('displayStyle -textured;')
    mel.eval('displayStyle -wireframeOnShaded;')
    cmds.file(rename='D:\\CubeMesh.ma')
    cmds.file(type='mayaAscii', save=True)
    
make_scene()

cmds.select('cube.f[0]', r=True)
cmds.polyInfo(faceNormals=True)
# Result: [u'FACE_NORMAL      0: 0.000000 0.000000 1.000000\n'] # 

cmds.select('cube.vtxFace[3][0]', r=True)
cmds.polyNormalPerVertex(q=True, xyz=True)
# Result: [0.0, 0.0, 1.0] # 
cmds.select('cube.vtx[3]', r=True)
cmds.polyNormalPerVertex(q=True, xyz=True)
# Result: [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0] # 

#calculate vertex normal
faces = cmds.polyInfo(vertexToFace=True)[0].strip()
print(faces)
#VERTEX      3:      1      0      4
import re
faces = re.findall(r'\d+', faces)[1:]

v_normal = [0,0,0]

for f in faces:
    f_normal = cmds.polyInfo('cube.f[%s]'%f, faceNormals=True)[0].strip()
    f_normal = f_normal.split(' ')[-3:]
    print(f_normal)
    f_normal = [float(n) for n in f_normal]
    print(f_normal)
    v_normal = map(lambda x,y:x+y, v_normal, f_normal)

print(v_normal)
# Result: [1.0, 1.0, 1.0] # 

import maya.OpenMaya as om
dir(om)
help(om.MVector)
vn = om.MVector(v_normal[0], v_normal[1], v_normal[2])
vn.normalize()
print(vn.x, vn.y, vn.z)
# Result: (0.5773502691896258, 0.5773502691896258, 0.5773502691896258) # 

#average vertex normal
import re
import maya.OpenMaya as om
def averageVertexNormal(verts):
    for v in verts:
        faces = cmds.polyInfo(v, vertexToFace=True)[0].strip()
        faces = re.findall(r'\d+', faces)[1:]
        vn = [0,0,0]
        for f in faces:
            fn = cmds.polyInfo('%s.f[%s]'%(v.split('.', 1)[0], f), faceNormals=True)[0].strip()
            fn = fn.split(' ')[-3:]
            fn = [float(n) for n in fn]
            vn = map(lambda x,y:x+y, vn, fn)
        vn = om.MVector(vn[0], vn[1], vn[2])
        vn.normalize()
        vn = (vn.x, vn.y, vn.z)
        cmds.polyNormalPerVertex(v, xyz=vn)
        
verts = cmds.filterExpand(sm=31)
if verts:
    averageVertexNormal(verts)
            