'''
Created on 24. 12. 2023

@author: mstolarz
'''
import importlib
from data import ca_file


def reload_it():
    importlib.reload(ca_file)    

    
    print ("Data reload: OK")