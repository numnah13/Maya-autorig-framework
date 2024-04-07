'''
Created on 27. 1. 2024

@author: theodox
https://stackoverflow.com/questions/76377828/how-to-rotate-a-node-from-a-custom-pivot/76411619#76411619
'''
import maya.api.OpenMaya as om
import maya.cmds as cmds

# from the question code...
object_position = om.MVector(0,1,0)
pivot_pos = om.MVector(0,0,0)
twist_axis = om.MVector(0.0, 0.0, 1.0)
twist_value = 1

# note that we set the translation to the _pivot pos_
transform = om.MTransformationMatrix()
transform.setTranslation(pivot_pos, om.MSpace.kWorld)

# get the relative position to the desired point
relative_pos = object_position * transform.asMatrixInverse()

# original rotation code remains the same
rotation_quat = om.MQuaternion(twist_value, twist_axis)
transform.rotateBy(rotation_quat, om.MSpace.kTransform)

# instead of checking the translation, 
# multiply the test point by the transform matrix
final_pos =  relative_pos * transform.asMatrix(1)

# Your locator pos will be rotated around the pivot you supplied
cmds.spaceLocator(p=(final_pos.x, final_pos.y, final_pos.z))