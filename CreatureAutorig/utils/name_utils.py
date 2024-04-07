# pylint: disable=trailing-whitespace

# pylint: disable=import-error
'''
@author: mstolarz
'''

import maya.OpenMaya as om
from maya import cmds
import autorig_settings as sett

def add_padding(start_num=1, end_num=1, padding=None, step=1, iterations=None) -> [str]:
    '''
    TODO: is this method really needed?
    The function adds zero padding for the given sequence of numbers
    @param start_num: int, first number that needs to have padding added
    @param end_num: int, the last number in the range that needs 
                    to have padding added (also included),
                    param disabled if iterations param is provided
    @param padding: int, number of characters in the final
    @param step: int, step in the range of numbers
    @param iterations: int, how many numbers need to have padding added
    @return [str]
    '''
    if padding is None:
        padding = sett.ZERO_PADDING
    
    result = []
    if iterations:
        it = 0
        while it < iterations:
            res = str(start_num).zfill(padding)
            result.append(res)
            it+=1
            start_num+=step        
    else:           
        for n in range(start_num, end_num+1, step):
            res = str(n).zfill(padding)
            result.append(res)
            
            
    return result


def build_unique_name(base_name, side, suffix, front_or_hind=None, 
                      ik_or_fk=None, suffix1=None, num=None):
    '''
    The function generates a name for any node following a consistent convension
    @param base_name: str, this is the base_name of the name, body part name
    @param side: str, this is the side of the name (available options defined in autorig_settings)
    @param suffix: str, main suffix (available options defined in autorig_settings)
    @param front_or_hind: str, front or hind (available options defined in autorig_settings)
    @param ik_or_fk: str, ik or fk (available options defined in autorig_settings)
    @param suffix1: str, additional suffix (available options defined in autorig_settings)
    @param num: int, number
    @return str: the generated name
    '''
    
    if not side in sett.sides:
        raise ValueError("Side is not valid")
  
    
    if not suffix in sett.suffixes:
        raise ValueError(f"{suffix} is not a valid suffix")
    
    if front_or_hind:
        if not front_or_hind in sett.suffixes:
            raise ValueError(f"{front_or_hind} is not a valid suffix")
        
    if ik_or_fk:
        if not ik_or_fk in sett.suffixes:
            raise ValueError(f"{ik_or_fk} is not a valid suffix")
    
    if suffix1:
        if not suffix1 in sett.suffixes:
            raise ValueError(f"{suffix1} is not a valid suffix")
    
    pad_num = None
    if num:
        pad_num = str(num).zfill(sett.ZERO_PADDING)
           
    name = "_".join(filter(None, [base_name, side, front_or_hind, 
                                  ik_or_fk, suffix1, suffix, pad_num]))
    
    name = __unique_name(name)
    return name
                     
    

def __unique_name(name):
    '''
    This method ensures the name is unique 
    '''
    
    security = 2000
    
    i = 1
    while cmds.objExists(name)==1:
        if i < security:            
            res = name.split("_")
            if res[-1].isnumeric():
                new_num = str(int(res[-1])+1).zfill(sett.ZERO_PADDING)
                name = "_".join(res[:-1]+[new_num])           
            else:
                num = str(i).zfill(sett.ZERO_PADDING)
                name = name +"_" + num
            i+=1
        
    return name


def check_name(name):
    '''
    TODO: not completed
    Checks if the given name follows the naming convention
    '''
    if name:
        res = name.split("_")
        if res[-1].isnumeric():
            if len(res[-1]) != sett.ZERO_PADDING:
                om.MGlobal.displayError("Name invalid. Wrong zero padding")
                return False
        else:
            if not res[-1] in sett.suffixes:
                om.MGlobal.displayError("Name invalid. Wrong suffix")
                return False
            

        return True
    
    return None



# DESIRED NAMES:
# foot_front_L_ik_ctrl         <- wildPig_front_L_foot_ctrl
# foot_hind_L_ik_ctrl          <- wildPig_hind_L_foot_ctrl
# foot_hind_L_fk_ctrl          <- wildPig_hind_foot_L_fk_ctrl
# legPV_front_L_ctrl ??        <- wildPig_front_L_elbow_PV_ctrl
# legPV_hind_L_ctrl ??         <- wildPig_hind_L_knee_PV_ctrl
# tail_fk_ctrl_01              <- wildPig_tail_fk_ctrl_01
#                     <- wildPig_front_L_shoulder_ik_ctrl
# hip_L_ik_ctrl                <- turkey_hind_L_hip_ik_ctrl
#                     <- wildPig_jaw_up_ctrl
# spine_fk_ctrl_01             <- wildPig_spine_fk_ctrl_01
# spine_ik_ctrl_02             <- wildPig_mid_spine_ctrl
#                     <- wildPig_rootJnt_ctrl
# leg_hind_config_ctrl         <- wildPig_hind_leg_L_settings_ctrl
#
#                                 <- turkey_wing_metacarpus_L_fk_ctrl
#                                 <- turkey_wing_digit_L_fk_ctrl
# featherE_L_fk_ctrl_01        <- turkey_feather5_L_fk_ctrl_01
#                             <- turkey_feather5_L_fk_ctrl_02
#                             <- turkey_breast_L_dyn_ctrl
#
#                             <- goat_ear_L_skin_jnt_02
#
# from utils import nameUtils
# #nameUtils.buildName(base_name, side, suffix, front_or_hind=None, 
#                         ik_or_fk=None, suffix1=None, num=None)
# name1 = nameUtils.buildName("foot", "R", "ctrl", front_or_hind="front", 
#                             ik_or_fk="ik", suffix1="config", num=2)
# name2 = nameUtils.buildName("featherE", "R", "ctrl", ik_or_fk="fk", num=1)
# name3 = nameUtils.buildName("ear", "L", "skinJnt",  num=2)
# name4 = nameUtils.buildName("spine", "M", "ctrl",  ik_or_fk="ik", num=7)
# name5 = nameUtils.buildName("leg", "L", "ctrl", front_or_hind="front", suffix1="config")
# print (name1)
# print (name2)
# print (name3)
# print (name4)
# print (name5)
