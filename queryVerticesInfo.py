#coding:utf-8
#queryVerticesInfo.py

import maya.cmds as cmds

#new scene
cmds.file(new=True, f=True)
cmds.polyPlane(w=5, h=5, sw=1, sh=1, n='square')
cmds.file(rn='BasicPolygon.ma')
cmds.file(type='mayaAscii', f=True, s=True)

#print all vertices position
count = cmds.polyEvaluate(vertex=True)
cmds.getAttr('square.vrts[0]') # Result: [(-2.5, -5.551115123125783e-16, 2.5)] # 
for i in range(count):
    pos = cmds.getAttr('%s.vrts[%d]'%(cmds.ls(sl=True)[0], i))[0]
    print('%.2f, %.2f, %.2f'%(pos[0], pos[1], pos[2]))
    
#another
coords = cmds.getAttr('square.vrts[*]')
# Result: [(-2.5, -5.551115123125783e-16, 2.5), (2.5, -5.551115123125783e-16, 2.5), (-2.5, 5.551115123125783e-16, -2.5), (2.5, 5.551115123125783e-16, -2.5)] # 
for pos in coords:
    print('%.2f, %.2f, %.2f'%(pos[0], pos[1], pos[-1]))
    
#
print(cmds.pointPosition('square.vtx[0]', local=True))
print(cmds.pointPosition('square.vtx[0]', world=True))
cmds.setAttr('square.translateY', 3)
print(cmds.pointPosition('square.vtx[0]', local=True)) #[-2.5, -5.551115123125783e-16, 2.5]
print(cmds.pointPosition('square.vtx[0]', world=True)) #[-2.5, 2.9999999999999996, 2.5]

#world space
cmds.pointPosition('square.vtx[0]') # Result: [-2.5, 2.9999999999999996, 2.5] # 
for i in range(cmds.polyEvaluate(vertex=True)):
    pos = cmds.pointPosition('%s.vtx[%d]'%(cmds.ls(sl=True)[0], i), world=True)
    print(pos)


