# coding:utf-8
# break all connections between mesh and initialShadingGroup
from maya.api import OpenMaya as om
from maya import cmds

selList = om.MGlobal.getActiveSelectionList()
iter = om.MItSelectionList(selList)
meshFn = om.MFnMesh()
while not iter.isDone():
    dagPath = iter.getDagPath()
    print(dagPath.fullPathName())
    meshFn.setObject(dagPath)
    shaders, faces = meshFn.getConnectedShaders(0)
    print(len(shaders))
    if len(shaders) > 1:
        for shader in shaders:
            dependencyNodeFn = om.MFnDependencyNode(shader)
            sg_name = dependencyNodeFn.name()
            if sg_name == u'initialShadingGroup':
                # break mesh and sg connections, eg:
                # disconnectAttr sm24_1004_CasinoBar01A_P001_metalShape.instObjGroups[0].objectGroups[0] initialShadingGroup.dagSetMembers[0];
                # disconnectAttr initialShadingGroup.memberWireframeColor sm24_1004_CasinoBar01A_P001_metalShape.instObjGroups[0].objectGroups[0].objectGrpColor;
                pass
    print('-'*40)
    iter.next()
    

dir(dependencyNodeFn)
dependencyNodeFn.name()



for plug in dependencyNodeFn.getConnections():
    dest = plug.connectedTo(True, False)
    for p in dest:
        print(plug.name() + '\t' + p.name())
        
    src = plug.connectedTo(False, True)
    for p in src:
        print(plug.name() + '\t' + p.name())

om.MFnDependencyNode(plug.node()).name()
shader == plug.node()

shader.
plug = dependencyNodeFn.findPlug('surfaceShader', True)
for p in plug.connectedTo(True, False):
    print(p.name())
dependencyNodeFn.getAffectedAttributes()

cmds.listConnections(obj)
cmds.listAttr(obj)
cmds.listConnections(u'initialShadingGroup', plugs=True)

obj = cmds.ls(sl=True)[0]
cmds.sets(obj, rm='initialShadingGroup');
