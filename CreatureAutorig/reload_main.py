'''
Created on 24. 12. 2023

@author: mstolarz
'''
import importlib
from core import reload_core
from modules import reload_modules
from ui import reload_ui
from utils import reload_utils
from data import reload_data
import autorig_settings


def reload_it():   
    importlib.reload(reload_core) 
    importlib.reload(reload_modules)   
    importlib.reload(reload_ui)
    importlib.reload(reload_utils)
    importlib.reload(reload_data)
    importlib.reload(autorig_settings)
    
    reload_core.reload_it()
    reload_modules.reload_it()
    reload_ui.reload_it()
    reload_utils.reload_it()
    reload_data.reload_it()
    
    print ("Main reload: OK")