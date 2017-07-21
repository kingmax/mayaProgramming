#coding:utf-8
#QueryFacesInfo.py

import maya.cmds as cmds

def make_scene():
    cmds.file(f=1, new=1)
    cmds.polyPlane(w=5, sw=2, h=5, sh=1, n="square")
    #cmds.polyConnectComponents('square.vtx[1:2]')
    cmds.file(rename='TwoPolygonMesh.ma')
    cmds.file(type='mayaAscii', save=1)
    

if __name__ == '__main__':
    make_scene()
    
    sels = cmds.ls(sl=1, dag=1, geometry=1, long=1)
    for node in sels:
        face_count = cmds.polyEvaluate(node,face=1)
        print('%s has %d faces.'%(node, face_count))
        
        for i in range(face_count):
            pi = cmds.polyInfo('%s.f[%d]'%(node, i), faceToVertex=1)[0].strip()
            print(pi)
            # Result: FACE      1:      1      2      5      4 # 
            pi = pi.split(':')[-1]
            import re
            verts = re.findall(r'\d+', pi)
            print('Face %d'%i)
            print(' # Verts:%d'%len(verts))
            for v_index in verts:
                pos = cmds.pointPosition('%s.vtx[%s]'%(node, v_index), world=1)
                print('%s: [%.2f, %.2f, %.2g]'%(v_index, pos[0], pos[1], pos[2]))

                
''' #output

|square|squareShape has 2 faces.
FACE      0:      0      1      4      3
Face 0
 # Verts:4
0: [-2.50, -0.00, 2.5]
1: [0.00, -0.00, 2.5]
4: [0.00, 0.00, -2.5]
3: [-2.50, 0.00, -2.5]
FACE      1:      1      2      5      4
Face 1
 # Verts:4
1: [0.00, -0.00, 2.5]
2: [2.50, -0.00, 2.5]
5: [2.50, 0.00, -2.5]
4: [0.00, 0.00, -2.5]

'''                
            