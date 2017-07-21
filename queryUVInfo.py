#coding:utf-8
#queryUVInfo.py

import maya.cmds as cmds
import maya.mel as mel

def make_scene():
    cmds.file(new=True, f=True)
    cmds.polyPlane(w=1, sw=2, h=1, sh=1, name="square")
    cmds.polyUVSet(create=True, uvSet="map2")
    cmds.polyUVSet(copy=True, uvSet="map1", newUVSet="map2")
    mel.eval("displayStyle -textured;")
    mel.eval("displayStyle -wireframeOnShaded;")
    cmds.file(rename="C:\\TwoPolygonMesh.ma")
    cmds.file(type="mayaAscii", save=True)
    
make_scene()

cmds.polyUVSet(q=True, allUVSets=True)
# Result: [u'map1', u'map2'] # 
cmds.polyUVSet(q=True, currentUVSet=True)

#
cmds.select('square.map[*]')
cmds.polyEditUV(q=True, u=True, v=True)
# Result: [0.0, 0.0, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 0.5, 1.0, 1.0, 1.0] # 
cmds.polyEditUV(u=1, v=1)
cmds.polyEditUV(q=True, u=True, v=True)
# Result: [1.0, 1.0, 1.5, 1.0, 2.0, 1.0, 1.0, 2.0, 1.5, 2.0, 2.0, 2.0] # 
cmds.polyEditUV(u=1, v=1, relative=False)
cmds.polyEditUV(q=True, u=True, v=True)
# Result: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] # 

#move selected uv
cmds.ls(sl=True)
# Result: [u'square.map[3:5]'] # 
cmds.filterExpand(sm=35)
# Result: [u'square.map[1]', u'square.map[3]', u'square.map[4]', u'square.map[5]'] # 
uvs = cmds.filterExpand(sm=35)
import random
for uv in uvs:
    print(uv)
    cmds.select(uv)
    cmds.polyEditUV(u=random.random(), v=random.random(), r=False)
    
cmds.select(uvs)
    
    