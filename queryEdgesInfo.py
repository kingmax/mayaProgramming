#coding:utf-8
#QueryEdgeInfo.py

import maya.cmds as cmds

def make_scene():
    cmds.file(f=True, new=True)
    cmds.polyPlane(w=5,sw=1,h=5,sh=1,name='square')
    cmds.file(rn='BasicPolygon.ma')
    cmds.file(type='mayaAscii', save=True)


if __name__ == '__main__':
    make_scene()
    
    #print all vertex of edge
    sels = cmds.ls(sl=True, dag=True, geometry=True, long=True)
    for node in sels:
        edge_count = cmds.polyEvaluate(node, edge=True)
        print('%s has %d edges.'%(node, edge_count))
        for i in range(edge_count):
            edge2vert = cmds.polyInfo('%s.e[%d]'%(node, i), edgeToVertex=True)[0]
            #cmds.polyInfo('square.e[0]', edgeToVertex=True)[0]
            # Result: EDGE      0:      0      1  Hard
            # # 
            import re
            edge_verts = re.findall(r'\d+', edge2vert)
            eg = edge_verts[0]
            v0 = edge_verts[1]
            v1 = edge_verts[2]
            print('edge:%s <=> verts:%s -> %s'%(eg, v0, v1))

############### output
'''
|square|squareShape has 4 edges.
edge:0 <=> verts:0 -> 1
edge:1 <=> verts:0 -> 2
edge:2 <=> verts:1 -> 3
edge:3 <=> verts:2 -> 3
'''
##########################

            