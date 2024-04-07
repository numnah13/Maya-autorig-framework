'''
Created on 24. 1. 2024

@author: Yantor3d
https://yantor3d.wordpress.com/2017/08/11/cmds-vs-openmaya/
'''
sel = OpenMaya.MSelectionList()
sel.add('skinCluster1')
sel.add('my_meshShape')  # The Maya API is picky about shape vs. transform

scls_obj = sel.getDependNode(0)
mesh_dag = sel.getDagPath(1)

fn_scls = OpenMayaAnim.MFnSkinCluster(scls_obj)

fn_comp = OpenMaya.MFnSingleIndexedComponent()
verts_obj = fn_comp.create(OpenMaya.MFn.kMeshVertComponent)
fn_comp.setCompleteData(OpenMaya.MFnMesh(mesh_dag).numVertices)

weights, numInfluences = fn_scls.getWeights(mesh_dag, verts_obj)



#get back to that map of joint->vertices?
# I'm not sure if there a better way to do this...
vertices = OpenMaya.MSelectionList().add((mesh_dag, verts_obj)).getSelectionStrings()
vertices = cmds.filterExpand(vertices, selectionMask=31)

joints = [each.partialPathName() for each in fn_scls.influenceObjects()]

influenced_vertices = defaultdict(list)

for vtx, wts in zip(vertices, weights):
    jnt, wt = sorted(zip(joints, wts), key=lambda jw: jw[1])[-1]
    influenced_vertices[jnt].append(vtx)