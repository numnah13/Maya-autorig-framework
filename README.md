import sys
import importlib

path = "D:/rigs/Marta/EclipseWorkspace/CreatureAutorigProject/CreatureAutorig"
if path not in sys.path:
    sys.path.append(path)
    
import reload_main
importlib.reload(reload_main)
reload_main.reload_it()
