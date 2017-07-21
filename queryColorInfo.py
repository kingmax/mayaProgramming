#coding:utf-8
#queryColorInfo.py

import maya.cmds as cmds
import maya.mel as mel

def make_scene():
    cmds.file(new=True, f=True)
    cmds.polyPlane(w=5, sw=2, h=5, sh=1, name='square')
    mel.eval("displayStyle -textured")
    mel.eval("displayStyle -wireframeOnShaded")
    cmds.file(rename='TwoPolygonMesh.ma')
    cmds.file(type='mayaAscii', save=True)
    cmds.polyOptions(colorShadedDisplay=True, colorMaterialChannel='none')
    
if __name__ == '__main__':
    make_scene()
    
    cmds.select('square.vtx[4]')
    cmds.polyColorPerVertex(rgb=(1,1,0))
    
    cmds.select('square.vtxFace[4][1]')
    cmds.polyColorPerVertex(rgb=(1,0,1), a=0.5)
    
    cmds.select('square.vtxFace[*][*]')
    cmds.polyColorPerVertex(q=True, rgb=True)
    # Result: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0] # 
    
    cmds.select('square.vtx[*]')
    cmds.polyColorPerVertex(q=True, rgb=True)
    # Result: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.5, 0.5, 0.0, 0.0, 0.0] # 
