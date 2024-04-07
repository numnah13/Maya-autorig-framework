'''
Created on 24. 12. 2023

@author: mstolarz
'''
import importlib
from ui import build_session_ui


def reload_it():
    importlib.reload(build_session_ui)

    print ("UI reload: OK")
