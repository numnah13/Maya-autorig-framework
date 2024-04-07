'''
Created on 3. 4. 2024

@author: mstolarz
'''
import pymel.core as pm
import autorig_settings as sett
from modules import control
import maya.OpenMaya as om

def create_all_controls(move_by=3):
    '''
    The function creates all controls defined in autorig_settings
    with all colors defined in autorig_settings.
    @param move_by: int, a unit by which controls are distributed in the scene in X axis
    '''
    ctrls_num = 0
    color_index = 0
    for i, shp in enumerate(sett.ctrl_shp_types):
        print (shp)      
        if color_index >= len(sett.colors):
            color_index = 0
        color_name = list(sett.colors)[color_index]
        ctrl = control.Control(base_name=shp, ctrl_color=color_name)
        try:
            ctrl.build(shp)
            pm.move(i*move_by,0,0, ctrl.control_grp)
        except ValueError as e:
            print("Error:", e)
        else:
            ctrls_num += 1
            color_index += 1

    om.MGlobal.displayInfo(f"{ctrls_num}/{len(sett.ctrl_shp_types)}: "
                           "controls created / shape names defined")

        