'''
Created on 24. 12. 2023

@author: mstolarz
'''
import importlib
from core import build_session


def reload_it():
    importlib.reload(build_session)   

    
    print ("Core reload: OK")
