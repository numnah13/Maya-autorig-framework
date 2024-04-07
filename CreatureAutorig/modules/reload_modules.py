'''
Created on 24. 12. 2023

@author: mstolarz
'''
import importlib

from modules import main_module
from modules import limb_module
from modules.submodules import control
from modules.submodules import joint_chain
from modules.submodules import ik_chain
from modules.submodules import fk_chain
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