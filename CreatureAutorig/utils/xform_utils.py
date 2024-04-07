# pylint: disable=import-error
'''
@author: mstolarz
'''
import maya.OpenMaya as om
import pymel.core as pm
from utils import name_utils


def zero(obj):
    '''
    TODO - this should take the number from the obj that's being grouped
    This function gets a pymel object and groups it 
    with the group aligned with that object to zero out the transforms
    @param obj: PyNode, the object to be zeroed out
    @return PyNode: the offset group
    '''

    #Get parent object

    par = obj.getParent()

    #Create gorup name
    name =  obj.name()
    temp = name.split("_")

    group_name = name_utils.build_unique_name(temp[0]+"Zero", temp[1], "grp")

    if not group_name:
        om.MGlobal.displayError("Failed to generate a group name")
        return None

    #Create the group
    grp = pm.createNode("transform", name=group_name)

    #Set the matrix for the group
    grp.setMatrix(obj.wm.get())

    #Rebuild hierarchy
    obj.setParent(grp)
    if par:
        grp.setParent(par)

    return grp


def zero_rotation(obj):
    '''
    TODO
    '''
    return True
