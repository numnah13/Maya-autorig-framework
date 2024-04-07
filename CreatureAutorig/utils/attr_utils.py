'''
Created on 24. 12. 2023

@author: mstolarz
'''
import pymel.core as pm

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
    

    
    # attrs_to_lock = []
    # for l in lock:
    #     if l in attr_dict

    
def get_attrs_to_lock_n_hide(lock, not_lock=None):
    valid = ["all", "a", "translate", "t", "rotate", "r", 
            "scale", "s", "visibility", "v",
            "translateX", "tx", "translateY", "ty", "translateZ", "tz",
            "rotateX", "rx", "rotateY", "ry", "rotateZ", "rz",
            "scaleX", "sx", "scaleY", "sy", "scaleZ", "sz",
            "visibility", "v", "x", "y", "z"]
    attr_dict = {"translateX": ["all", "a", "translate", "t", "translateX", "tx", "x"],
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
    if any(l for l in lock not in valid):
        raise ValueError ("Invalid input")
    
    print (lock)
    
    # matching_keys = []
    # for key, values in attr_dict.items():
    #     if any(val in valid for val in values):
    #         matching_keys.append(key)
    # return matching_keys


def lock_and_hide2(obj, attrs=["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]):
    for a in attrs:
        obj.attr(a).lock()
        obj.attr(a).setKeyable(0)
        obj.attr(a).showInChannelBox(0)