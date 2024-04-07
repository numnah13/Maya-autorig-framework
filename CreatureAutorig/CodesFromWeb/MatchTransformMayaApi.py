'''
Created on 24. 1. 2024

@author: RIHAM TOULAN
https://www.rihamtoulan.com/blog/2017/12/21/matching-transformation-in-maya-and-mfntransform-pitfalls
'''


import maya.api.OpenMaya as OpenMaya

def getMDagPath(node):
    selList=OpenMaya.MSelectionList()
    selList.add(node)
    return selList.getDagPath(0)
    
def getMObject(node):
    selList=OpenMaya.MSelectionList()
    selList.add(node)
    return selList.getDependNode(0)

def matchTranformation(targetNode, followerNode, translation=True, rotation=True):
    followerMTransform=OpenMaya.MFnTransform(getMDagPath(followerNode))
    targetMTransform=OpenMaya.MFnTransform(getMDagPath(targetNode))
    targetMTMatrix=OpenMaya.MTransformationMatrix(OpenMaya.MMatrix(cmds.xform(targetNode, matrix=True, ws=1, q=True)))
    if translation:
        targetRotatePivot=OpenMaya.MVector(targetMTransform.rotatePivot(OpenMaya.MSpace.kWorld))
        followerMTransform.setTranslation(targetRotatePivot,OpenMaya.MSpace.kWorld)
    if rotation:
        #using the target matrix decomposition
        #Worked on all cases tested
        followerMTransform.setRotation(targetMTMatrix.rotation(True),OpenMaya.MSpace.kWorld)
        
        #Using the MFnTransform quaternion rotation in world space
        #Doesn't work when there is a -1 scale on the object itself
        #Doesn't work when the object has frozen transformations and there is a -1 scale on a parent group.
        #followerMTransform.setRotation(MFntMainNode.rotation(OpenMaya.MSpace.kWorld, asQuaternion=True),OpenMaya.MSpace.kWorld)
        
        
        
        
        