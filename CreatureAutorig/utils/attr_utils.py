'''
Created on 24. 12. 2023

@author: mstolarz
'''
import pymel.core as pm
import maya.OpenMaya as om


VALID_INPUT = ["all", "a", "translate", "t", "rotate", "r", 
        "scale", "s", "visibility", "v",
        "translateX", "tx", "translateY", "ty", "translateZ", "tz",
        "rotateX", "rx", "rotateY", "ry", "rotateZ", "rz",
        "scaleX", "sx", "scaleY", "sy", "scaleZ", "sz",
        "visibility", "v", "x", "y", "z"]
ATTR_REMAP = {"translateX": ["all", "a", "translate", "t", "translateX", "tx", "x"],
             "translateY": ["all", "a", "translate", "t", "translateY", "ty", "y"],
             "translateZ": ["all", "a", "translate", "t", "translateZ", "tz", "z"],
             "rotateX": ["all", "a", "rotate", "r", "rotateX", "rx", "x"],
             "rotateY": ["all", "a", "rotate", "r", "rotateY", "ry", "y"],
             "rotateZ": ["all", "a", "rotate", "r", "rotateZ", "rz", "z"],
             "scaleX": ["all", "a", "scale", "s", "scaleX", "sx", "x"],
             "scaleY": ["all", "a", "scale", "s", "scaleY", "sy", "y"],
             "scaleZ": ["all", "a", "scale", "s", "scaleZ", "sz", "z"],
             "visibility": ["all", "a", "visibility", "v"]
             }



def get_flat_list(*input_vals):
    '''
    The function takes multiple inputs in various form and returns a single flat list 
    of all the items found in nested lists or tuples.
    It does not unpack sets and dictionaries.
    @param input_vals: a single or multiple variables of different type
    @return: list: flat-structured list                    
    '''    
    input_vals = list(input_vals)
    flat_list = flatten_list_recursion(input_vals)

    return flat_list


def flatten_list_recursion(nested_list):
    '''
    The function takes a nested list or tuple and returns a flat list of all the items
    using recursion. It does not unpack sets and dictionaries
    @param nested_list: a list or a tuple which can (but doesn't have to) contain
                        other lists, tuples
    @return: list: flat-structured list                    
    '''
    flattened = []
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            flattened.extend(flatten_list_recursion(item))
        else:
            flattened.append(item)
    return flattened


def validate_input(input_list):
    '''
    The function checks if the names of attributes are valid.
    If the parameters are not in a list, the
    @param input_list: a flat list of strings
    '''
    input_list = list(set(input_list))
    invalid_items = []
    for item in input_list:
        if item not in VALID_INPUT:
            invalid_items.append(item)
    if invalid_items:
        raise ValueError(f"Invalid values: {', '.join(map(str, invalid_items))}")

    return True


def remap_input(input_list):
    '''
    This method takes the validated input and checks each item in the list
    for the key it represents in the dictionary ATTR_REMAP
    '''
    attrs = []
    if "all" in input_list or "a" in input_list:
        return list(ATTR_REMAP.keys())
        
        
    for key, values in ATTR_REMAP.items():
        for item in input_list:
            if item in values:
                attrs.append(key)
                
    attrs = list(set(attrs))
    attrs.sort(key=sort_by_key_index)
    
    return attrs
        
def sort_by_key_index(attr):
    '''
    This function returns index of a key in a dictionary ATTR_REMAP
    '''
    
    return list(ATTR_REMAP.keys()).index(attr)            


def lock_and_hide(obj, lock=["all"], not_lock=None):
    '''
    The function locks and hide object's attributes in the Channel Box
    The function adds up all the attributes defined in the 'lock' parameter
    and from that it extracts all the attributes defined in the 'not_lock' parameter.
    This way it gets the list of the attributes which should be locked and hidden.
    @param lock: [str] takes values: all, a, translate, t, rotate, r, 
                                    scale, s, visibility, v,
                                    translateX, tx, translateY, ty, 
                                    translateZ, tz,
                                    rotateX, rx, rotateY, ry, 
                                    rotateZ, rz,
                                    scaleX, sx, scaleY, sy, 
                                    scaleZ, sz,
                                    visibility, v, x, y, z
    @param not_lock: [str] takes values: all, a, translate, t, rotate, r, 
                                scale, s, visibility, v,
                                translateX, tx, translateY, ty, 
                                translateZ, tz,
                                rotateX, rx, rotateY, ry, 
                                rotateZ, rz,
                                scaleX, sx, scaleY, sy, 
                                scaleZ, sz,
                                visibility, v, x, y, z
    '''
    
    if not obj:
        raise ValueError("Object not defined")
    if not pm.objExists(obj):
        raise ValueError(f"Object '{obj}' does not exist")
    
    lock_input = get_flat_list(lock)
    try:
        validate_input(lock_input)
    except ValueError as e:
        om.MGlobal.displayError(e)
        return None        
    lock_attrs = remap_input(lock_input)

    not_lock_input = get_flat_list(not_lock)
    try:
        validate_input(not_lock_input)
    except ValueError as e:
        om.MGlobal.displayError(e)
        return None        
    not_lock_attrs = remap_input(not_lock_input)

    attrs_to_lock = list(set(lock_attrs)-set(not_lock_attrs))
    attrs_to_lock.sort(key=sort_by_key_index)

    for a in attrs_to_lock:
        obj.attr(a).lock()
        obj.attr(a).setKeyable(0)
        obj.attr(a).showInChannelBox(0)


