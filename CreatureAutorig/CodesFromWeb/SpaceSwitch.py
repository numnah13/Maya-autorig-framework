'''
Created on 24. 1. 2024

@author: Chad Vernon
https://www.chadvernon.com/blog/space-switching-offset-parent-matrix/
'''

# To maintain the offset when creating the setup, we need to create an offset matrix relative to the parent:
offset = (
    OpenMaya.MMatrix(cmds.getAttr("{}.worldMatrix[0]".format(child)))
    * OpenMaya.MMatrix(cmds.getAttr("{}.matrix".format(child))).inverse()
    * OpenMaya.MMatrix(cmds.getAttr("{}.worldInverseMatrix[0]".format(parent)))
)

'''
Since the offsetParentMatrix is applied in local space, we need to then multiply the result
 by the child's parent inverse matrix. However, there seems to be cycle evaluation issues 
 when using a node's parentInverse to calculate the offsetParentMatrix, so you can use the actual 
 parent's world inverse matrix instead. I'm not sure if the parentInverse evaluation issue is a bug 
 or not but we have a work around. NO IT'S NOT A BUG This is by design. From Will Telford, Maya Senior Product owner: 
 “The parentMatrix output concatenates the OPM with the parentMatrix. This allows things like 
 existing constraints to continue to function." Here is the multMatrix setup scripted out:
'''
mult = cmds.createNode("multMatrix")

offset = matrix_to_list(
    OpenMaya.MMatrix(cmds.getAttr("{}.worldMatrix[0]".format(node)))
    * OpenMaya.MMatrix(cmds.getAttr("{}.matrix".format(node))).inverse()
    * OpenMaya.MMatrix(cmds.getAttr("{}.worldInverseMatrix[0]".format(driver)))
)
cmds.setAttr("{}.matrixIn[0]".format(mult), offset, type="matrix")

cmds.connectAttr("{}.worldMatrix[0]".format(driver), "{}.matrixIn[1]".format(mult))

parent = cmds.listRelatives(node, parent=True, path=True)
if parent:
    cmds.connectAttr("{}.worldInverseMatrix[0]".format(parent[0]), "{}.matrixIn[2]".format(mult))

cmds.connectAttr(
    "{}.matrixSum".format(mult), "{}.offsetParentMatrix".format(node)
)