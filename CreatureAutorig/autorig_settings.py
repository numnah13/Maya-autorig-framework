'''
Created on 24. 12. 2023

@author: mstolarz
'''


ROOT_PATH = "D:/rigs/Marta/EclipseWorkspace/CreatureAutorigProject/CreatureAutorig/"
CORE_PATH = ROOT_PATH + "core/"
MODULES_PATH = ROOT_PATH + "modules/"
UI_PATH = ROOT_PATH + "ui/"
UTILS_PATH = ROOT_PATH + "utils/"
DATA_PATH = ROOT_PATH + "data/"

sides = {"M":"M", "L":"L", "R":"R"}
#sides = ("M", "L", "R")

# suffixes = ( "ctrl",
#              "jnt",
#              "skinJnt",
#              "grp",
#              "zero", #group which zeroes out transforms
#              "off", #additional group underneath zeroGroup
#              "loc",
#              "geo",
#              "crv",
#              "drvCrv",
#              "config",
#              "bshp",
#              "guide",
#              "plug",
#              "meta",
#              )
#ikFkSuffixes = ("ik", "fk")
#frontHindSuffixes = ("front", "hind")


suffixes = {"ctrl": "ctrl",
            "jnt": "jnt",
            "skinJnt": "skinJnt",
            "grp": "grp",
            "zero": "zero", #group which zeroes out transforms
            "off": "off", #additional group underneath zeroGroup
            "loc": "loc",
            "geo": "geo",
            "crv": "crv",
            "drvCrv": "drvCrv",
            "ik": "ik",
            "fk": "fk",
            "config": "config",
            "bshp": "bshp", #blendshape target
            "guide": "guide", #guide curve
            "plug": "plug", #module plug
            "meta": "meta", #meta data
            "front": "front",
            "hind": "hind",
            "up": "up",
            "low": "low",
            "lyr": "lyr" #display layer
            }

ZERO_PADDING = 2 #padding used to generate names

colors = {  "red": [2.0, 0.0, 0.0],
            "redDark": [0.522, 0.004, 0.004],
            "redLight": [4.679, 0.446, 0.357],
            "blue": [0.0, 0.0, 2.0],
            "blueDark": [0.010, 0.009, 0.572],
            "blueLight": [0.0, 2.0, 2.0],
            "green": [0.1, 2.0, 0.1],
            "greenDark": [0.0, 0.4, 0.0],
            "greenLight": [0.7, 2.0, 0.3],
            "yellow": [2.0, 2.0, 0.0],
            "yellowDark": [0.619, 0.55, 0.0],
            "yellowLight": [5.0, 5.0, 0.6],
            "orange": [2.5, 0.4, 0.0],
            "orangeDark": [0.619, 0.204, 0.0],
            "orangeLight": [4.515, 0.686, 0.177],
            "purple": [3.0, 0.15, 0.584],
            "purpleDark": [0.72, 0.02, 0.29],
            "purpleLight": [2.0, 0.5, 0.683],           
            "grey": [0.341, 0.341, 0.341],
            "black": [0.0, 0.0, 0.0],
            "white": [2.0, 2.0, 2.0]
            }

ctrl_shp_types = ["circle", "triangle", "square", "rectangle", "rectangleRound", "saddle",
                "cross", "crossThin", "crossFat", "star", "starThin", "starFat", 
                "arrowSingle", "arrowPointing", "arrowDouble", "arrowDoubleSpherical", 
                "arrowQuadruple", "arrowQuadrupleRound", 
                "catFoot", "horseFoot", "cowFoot", "birdFoot", 
                "wave", "pinCircle", "pinDiamond", 
                "sphere", "hemisphere", "cylinder", "cylinderPointing", 
                "cube", "cubeX", "cubeY", "cubeZ", "cuboid", 
                "diamond", "pyramid", "pyramidPointing", "axes"]

'''
# test colors
import autorig_settings as sett
import pymel.core as pm

x = 0
for key in sett.colors:
    myCircle = pm.circle(c=(x,0,0), ch=0, n=key)
    x+=3

    myCircle[0].overrideEnabled.set(1)
    myCircle[0].overrideRGBColors.set(1)
    myCircle[0].overrideColorRGB.set(sett.colors[key])
    
    myCircle[0].getShape().overrideEnabled.set(1)
    myCircle[0].getShape().overrideRGBColors.set(1)
    myCircle[0].getShape().overrideColorRGB.set(sett.colors[key])
    
    myCircle[0].getShape().lineWidth.set(3)
'''
