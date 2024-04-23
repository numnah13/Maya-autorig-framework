'''
Created on 24. 12. 2023

@author: mstolarz
'''
import importlib

from modules import main_module, limb_module
from modules.submodules import control, joint_chain, ik_chain, fk_chain
from modules.test_modules import test_control, test_joint_chain


def reload_it():
    importlib.reload(main_module)    
    importlib.reload(limb_module)    
    importlib.reload(control)
    importlib.reload(joint_chain)
    importlib.reload(ik_chain)
    importlib.reload(fk_chain)
    importlib.reload(test_control)
    importlib.reload(test_joint_chain)
    
    print ("Modules reload: OK")