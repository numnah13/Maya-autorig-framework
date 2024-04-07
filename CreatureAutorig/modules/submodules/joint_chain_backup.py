'''
Created on 24. 12. 2023

@author: mstolarz
'''


import pymel.core as pm
import maya.OpenMaya as om1
import maya.api.OpenMaya as om2
from utils import name_utils
import autorig_settings as sett
import math




class JointChain(object):
    def __init__(self, base_name="chain", side="M", num=1):
        '''
        This is the constructor
        @param base_name: string, the base name used to generate the names
        @param side: string, the side used to generate names
        @param num: int, the first number to start counting from
        '''
        
        self.base_name = base_name
        self.side = side
        self.num = num
        self.chain = []

    
    def __str__(self):
    
        chain_names = [obj.name() for obj in self.chain]
        result = "JointChain class: joints number: {}, joints: {}".format(self.chainLength(), chain_names)
    
        return result
    
    
    def __zero_orient_joint(self, joint):
        '''
        This method zeroes out the jointOrient attribute of a joint
        @param joint: PyNode, the joint which needs to have orientation zeroed out
        '''
    
        for a in ["jointOrientX", "jointOrientY", "jointOrientZ"]:
            joint.attr(a).set(0)


    def __make_hierarchy(self):
        "This method parents joints into a hierarchy"
        
        reversed_list = list(self.chain)
        reversed_list.reverse()
        for i in range(len(reversed_list)-1):
            pm.parent(reversed_list[i], reversed_list[i+1])
            
        pm.select(cl=1)
        
    
    def arbitraryChain(self, pos_list=[], orient_list=[], zero_orient_last=False, skip_last=False):
        '''
        This method builds a joint chain from a list of positions and orientations
        @param pos_list: float[3] list, the position list needed for the chain
        @param orient_list: float[3] list, the orientation list needed for the chain
        @param zero_orient_last: bool, whether or not zero out joint orientations of the last joint 
                                in the created chain, regardless the value of skip_last parameter
        '''
        if not pos_list:
            om1.displayError("Position list not defined")
            return

        if not orient_list:
            om1.displayError("Orientation list not defined")
            return
        
        if len(pos_list) != len(orient_list):
            om1.MGlobal.displayError("The list of positions and list of orientations should contain same number of items")
            return
        
        range_end = len(pos_list)
        if skip_last:
            range_end = len(pos_list)-1
        
        for i in range(range_end):
            name = name_utils.build_unique_name(self.base_name, self.side, sett.suffixes["jnt"])   
            pm.select(cl=1)    
            jnt = pm.joint(n=name, position=pos_list[i], orientation=orient_list[i])    
            self.chain.append(jnt)
    
        self.__make_hierarchy()

        if zero_orient_last:
            self.__zero_orient_joint(self.chain[-1])


    def linear_chain(self, pos_list=[], aim_axis="+x", upAxis="+y", upVec=None, skip_last=False, round_pos=10):
        
        if len(pos_list) < 2:
            om2.MGlobal.displayError("There has to be at least 2 positions defined. Found: {}".format(len(pos_list)))
            return
        
        if not upVec:
            om2.MGlobal.displayError("Up vector not defined")
            return
        
        valid = ["+x", "-x", "+y", "-y", "+z", "-z"]
        if aim_axis not in valid:
            om2.MGlobal.displayError("Incorrect value for aim_axis. Choose one string from: '+x', '-x', '+y', '-y', '+z', '-z'")
            return
        if upAxis not in valid:
            om2.MGlobal.displayError("Incorrect value for aim_axis. Choose one string from: '+x', '-x', '+y', '-y', '+z', '-z'")
            return
        if aim_axis[1] == upAxis[1]:
            om2.MGlobal.displayError("Attributes aim_axis and upAxis cannot share same axis")
            return

        #determine the range
        range_end = len(pos_list)
        if skip_last:
            range_end = len(pos_list)-1        
        
        if range_end > 2:
            if not self.check_collinear(pos_list):
                om2.MGlobal.displayError("The given positions are not collinear")
                return
            
        
        #get up vector
        if "-" in upAxis:
            upVec = upVec * -1
        upVec.normalize()       

        #calculate aim vector
        vec_start = om2.MVector(pos_list[0][0],pos_list[0][1],pos_list[0][2])
        vec_end = om2.MVector(pos_list[1][0],pos_list[1][1],pos_list[1][2])
                
        aim_vec = vec_end - vec_start
        if "-" in aim_axis:
            aim_vec = vec_start - vec_end
        aim_vec.normalize()
        
        # check if aim and up vector are perpendicular
        cross_prod = om2.MVector(aim_vec ^ upVec)
        if round(cross_prod.length(),round_pos) < 1.0:
            om2.MGlobal.displayError("Aim vector and up vector are not perpendicular to each other. Change aim_axis or upVec attribute and try again. ")
            return

        #create a matrix to orient joints
        if "x" in aim_axis and "y" in upAxis:
            third_vec = aim_vec ^ upVec 
            third_vec.normalize()
            matrix_vec = [aim_vec.x, aim_vec.y, aim_vec.z, 0,
                       upVec.x, upVec.y, upVec.z, 0,
                       third_vec.x, third_vec.y, third_vec.z, 0,                                                     
                        0,0,0,1]
        elif "x" in aim_axis and "z" in upAxis:
            third_vec = upVec ^ aim_vec 
            third_vec.normalize()
            matrix_vec = [aim_vec.x, aim_vec.y, aim_vec.z, 0,                               
                       third_vec.x, third_vec.y, third_vec.z, 0,
                       upVec.x, upVec.y, upVec.z, 0,                                                
                        0,0,0,1]             
        elif "y" in aim_axis and "x" in upAxis:
            third_vec = aim_vec ^ upVec 
            third_vec.normalize()
            matrix_vec = [upVec.x, upVec.y, upVec.z, 0,
                       aim_vec.x, aim_vec.y, aim_vec.z, 0,
                       third_vec.x, third_vec.y, third_vec.z, 0,                                                     
                        0,0,0,1]
        elif "y" in aim_axis and "z" in upAxis:
            third_vec = aim_vec ^ upVec 
            third_vec.normalize()
            matrix_vec = [third_vec.x, third_vec.y, third_vec.z, 0,
                       aim_vec.x, aim_vec.y, aim_vec.z, 0,
                       upVec.x, upVec.y, upVec.z, 0,                                                                                    
                        0,0,0,1]
        elif "z" in aim_axis and "x" in upAxis:
            third_vec = aim_vec ^ upVec 
            third_vec.normalize()                 
            matrix_vec = [upVec.x, upVec.y, upVec.z, 0,
                       third_vec.x, third_vec.y, third_vec.z, 0,                                                       
                       aim_vec.x, aim_vec.y, aim_vec.z, 0,                                                    
                        0,0,0,1]
        elif "z" in aim_axis and "y" in upAxis:
            third_vec = upVec ^ aim_vec 
            third_vec.normalize()
            matrix_vec = [third_vec.x, third_vec.y, third_vec.z, 0,
                       upVec.x, upVec.y, upVec.z, 0,                              
                       aim_vec.x, aim_vec.y, aim_vec.z, 0,                                                    
                        0,0,0,1]
        
        matrix_m = om2.MMatrix(matrix_vec)
        matrix_fn = om2.MTransformationMatrix(matrix_m)               
        
        #set joints rotations out of matrix
        rot_rad = matrix_fn.rotation(asQuaternion=False)              
        rot_deg = list(map(math.degrees, rot_rad))    
            
        #create joints in the correct positions
        for i in range(range_end):
            name = name_utils.build_unique_name(self.base_name, self.side, sett.suffixes["jnt"])
            pm.select(cl=1)
            jnt = pm.joint(n=name, position=pos_list[i])
            self.chain.append(jnt)
        
        #orient joints        
        i = 0
        while True: # emulation of do-while loop
            pm.xform(self.chain[i], ws=1, rotation=(rot_deg[0],
                                                    rot_deg[1],
                                                    rot_deg[2]))                                                          
            pm.makeIdentity(self.chain[i], apply=True, jointOrient=False, rotate=True)
            i += 1
            if i >= range_end-1:
                break
        
        self.__make_hierarchy()
        if len(self.chain) > 1:
            self.__zero_orient_joint(self.chain[-1])
        pm.select(cl=1)
   
        
    @staticmethod
    def linear_chain_test():
        '''
        Create a few locators and twist the first one. Select all the locators. 
        Orientation of the first one is going to be a twist reference object
        Edit vec variable to get twist object axis as an up vector for the chain:
        vecs[0] - it is X axis of the object, vecs[1] - Y axis, vecs[2] - Z axis
        Edit skip_last attribute to decide how the test is supposed to run
        '''
        
        pos_list = [pm.xform(item, q=1, ws=1, t=1) for item in pm.selected()]
        vecs = JointChain.getVecFromOri(pm.selected()[0])        
        vec = vecs[0] # run test for this reference object axis
        skip_last = False
        
        # X?
        chain1 = JointChain("plusX_plusY")
        chain1.linear_chain(pos_list, aim_axis="+x", upAxis="+y", upVec=vec, skip_last=skip_last)
        chain2 = JointChain("plusX_minusY")
        chain2.linear_chain(pos_list, aim_axis="+x", upAxis="-y", upVec=vec, skip_last=skip_last)
        chain3 = JointChain("minusX_plusY")
        chain3.linear_chain(pos_list, aim_axis="-x", upAxis="+y", upVec=vec, skip_last=skip_last)
        chain4 = JointChain("minusX_minusY")
        chain4.linear_chain(pos_list, aim_axis="-x", upAxis="-y", upVec=vec, skip_last=skip_last)
        
        chain5 = JointChain("plusX_plusZ")
        chain5.linear_chain(pos_list, aim_axis="+x", upAxis="+z", upVec=vec, skip_last=skip_last)
        chain6 = JointChain("plusX_minusZ")
        chain6.linear_chain(pos_list, aim_axis="+x", upAxis="-z", upVec=vec, skip_last=skip_last)
        chain7 = JointChain("minusX_plusZ")
        chain7.linear_chain(pos_list, aim_axis="-x", upAxis="+z", upVec=vec, skip_last=skip_last)
        chain8 = JointChain("minusX_minusZ")
        chain8.linear_chain(pos_list, aim_axis="-x", upAxis="-z", upVec=vec, skip_last=skip_last)
        
        # Y?
        chain9 = JointChain("plusY_plusX")
        chain9.linear_chain(pos_list, aim_axis="+y", upAxis="+x", upVec=vec, skip_last=skip_last)
        chain10 = JointChain("plusY_minusX")
        chain10.linear_chain(pos_list, aim_axis="+y", upAxis="-x", upVec=vec, skip_last=skip_last)
        chain11 = JointChain("minusY_plusX")
        chain11.linear_chain(pos_list, aim_axis="-y", upAxis="+x", upVec=vec, skip_last=skip_last)
        chain12 = JointChain("minusY_minusX")
        chain12.linear_chain(pos_list, aim_axis="-y", upAxis="-x", upVec=vec, skip_last=skip_last)
        
        chain13 = JointChain("plusY_plusZ")
        chain13.linear_chain(pos_list, aim_axis="+y", upAxis="+z", upVec=vec, skip_last=skip_last)
        chain14 = JointChain("plusY_minusZ")
        chain14.linear_chain(pos_list, aim_axis="+y", upAxis="-z", upVec=vec, skip_last=skip_last)
        chain15 = JointChain("minusY_plusZ")
        chain15.linear_chain(pos_list, aim_axis="-y", upAxis="+z", upVec=vec, skip_last=skip_last)
        chain16 = JointChain("minusY_minusZ")
        chain16.linear_chain(pos_list, aim_axis="-y", upAxis="-z", upVec=vec, skip_last=skip_last)
        
        # Z?
        chain17 = JointChain("plusZ_plusX")
        chain17.linear_chain(pos_list, aim_axis="+z", upAxis="+x", upVec=vec, skip_last=skip_last)
        chain18 = JointChain("plusZ_minusX")
        chain18.linear_chain(pos_list, aim_axis="+z", upAxis="-x", upVec=vec, skip_last=skip_last)
        chain19 = JointChain("minusZ_plusX")
        chain19.linear_chain(pos_list, aim_axis="-z", upAxis="+x", upVec=vec, skip_last=skip_last)
        chain20 = JointChain("minusZ_minusX")
        chain20.linear_chain(pos_list, aim_axis="-z", upAxis="-x", upVec=vec, skip_last=skip_last)
        
        chain21 = JointChain("plusZ_plusY")
        chain21.linear_chain(pos_list, aim_axis="+z", upAxis="+y", upVec=vec, skip_last=skip_last)
        chain22 = JointChain("plusZ_minusY")
        chain22.linear_chain(pos_list, aim_axis="+z", upAxis="-y", upVec=vec, skip_last=skip_last)
        chain23 = JointChain("minusZ_plusY")
        chain23.linear_chain(pos_list, aim_axis="-z", upAxis="+y", upVec=vec, skip_last=skip_last)
        chain24 = JointChain("minusZ_minusY")
        chain24.linear_chain(pos_list, aim_axis="-z", upAxis="-y", upVec=vec, skip_last=skip_last)
        
        
        

    def planarChain(self, pos_list=[], aim_axis="+x", upAxis="+y", skip_last=False):
        '''
        This method builds a joint chain from a list of positions and orientations
        @param pos_list: float[3] list, the position list needed for the chain
        @param aim_axis: string, axis going down the chain, accepts values: ["+x", "-x", "+y", "-y", "+z", "-z"]
        @param upAxis: string, secondary axis controling the twist, accepts values: ["+x", "-x", "+y", "-y", "+z", "-z"] 
        @param upVector: float[3], a direction at which upAxis should aim
        @param skip_last: bool, if set to True, the last joint will aim at the last position in pos_list,
                                if set to False, it will automatically zero out joint orientation of the last joint
        '''
        if not pos_list:
            om1.displayError("Position list not defined")
            return
        
        valid = ["+x", "-x", "+y", "-y", "+z", "-z"]
        if aim_axis not in valid:
            om1.MGlobal.displayError("Incorrect value for aim_axis. Choose one string from: '+x', '-x', '+y', '-y', '+z', '-z'")
            return
        if upAxis not in valid:
            om1.MGlobal.displayError("Incorrect value for aim_axis. Choose one string from: '+x', '-x', '+y', '-y', '+z', '-z'")
            return
        if aim_axis[1] == upAxis[1]:
            om1.MGlobal.displayError("Attributes aim_axis and upAxis cannot share same axis")
            return
        if not self.check_coplanar(pos_list):
            om1.MGlobal.displayError("The given positions are not coplanar")
            return
        
        #determine the range
        range_end = len(pos_list)
        if skip_last:
            range_end = len(pos_list)-1
        
        #create joints in the correct positions
        for i in range(range_end):
            name = name_utils.build_unique_name(self.base_name, self.side, sett.suffixes["jnt"])    
            pm.select(cl=1)
            jnt = pm.joint(n=name, position=pos_list[i])
            self.chain.append(jnt)
        
        #orient joints
        if "-" in upAxis:
            self.upVec = self.upVec * -1
            
        for i in range(len(self.chain)):
            if i < len(pos_list)-1: 
                vec_start = om1.MVector(pos_list[i][0],pos_list[i][1],pos_list[i][2])
                vec_end = om1.MVector(pos_list[i+1][0],pos_list[i+1][1],pos_list[i+1][2])
                
                #calculate aim vector
                aim_vec = vec_end - vec_start
                if "-" in aim_axis:
                    aim_vec = vec_start - vec_end
                aim_vec.normalize()
                  
                #calculate third vector
                third_vec = aim_vec ^ self.upVec
                third_vec.normalize()

                               
                #create a matrix
                if "x" in aim_axis and "y" in upAxis:
                    matrix_vec = [aim_vec.x, aim_vec.y, aim_vec.z, 0,
                               self.upVec.x, self.upVec.y, self.upVec.z, 0,
                               third_vec.x, third_vec.y, third_vec.z, 0,                                                     
                                0,0,0,1]
                elif "x" in aim_axis and "z" in upAxis:
                    matrix_vec = [aim_vec.x, aim_vec.y, aim_vec.z, 0,                               
                               third_vec.x, third_vec.y, third_vec.z, 0,
                               self.upVec.x, self.upVec.y, self.upVec.z, 0,                                                
                                0,0,0,1]             
                elif "y" in aim_axis and "x" in upAxis:
                    matrix_vec = [self.upVec.x, self.upVec.y, self.upVec.z, 0,
                               aim_vec.x, aim_vec.y, aim_vec.z, 0,
                               third_vec.x, third_vec.y, third_vec.z, 0,                                                     
                                0,0,0,1]
                elif "y" in aim_axis and "z" in upAxis:
                    matrix_vec = [third_vec.x, third_vec.y, third_vec.z, 0,
                               aim_vec.x, aim_vec.y, aim_vec.z, 0,
                               self.upVec.x, self.upVec.y, self.upVec.z, 0,                                                                                    
                                0,0,0,1]
                elif "z" in aim_axis and "x" in upAxis:                  
                    matrix_vec = [self.upVec.x, self.upVec.y, self.upVec.z, 0,
                               third_vec.x, third_vec.y, third_vec.z, 0,                                                       
                               aim_vec.x, aim_vec.y, aim_vec.z, 0,                                                    
                                0,0,0,1]
                elif "z" in aim_axis and "y" in upAxis:
                    matrix_vec = [third_vec.x, third_vec.y, third_vec.z, 0,
                               self.upVec.x, self.upVec.y, self.upVec.z, 0,                              
                               aim_vec.x, aim_vec.y, aim_vec.z, 0,                                                    
                                0,0,0,1]
               
                matrix_m = om1.MMatrix()
                om1.MScriptUtil.createMatrixFromList(matrix_vec, matrix_m)
                matrix_fn = om1.MTransformationMatrix(matrix_m)
                               
                #set joints rotations out of matrix
                rot_rad = matrix_fn.eulerRotation()              
                rot_deg = list(map(math.degrees, rot_rad))
                pm.xform(self.chain[i], ws=1, rotation=(rot_deg[0],
                                                        rot_deg[1],
                                                        rot_deg[2]))
                                                              
                pm.makeIdentity(self.chain[i], apply=True, jointOrient=False, rotate=True)
        
        self.__make_hierarchy()
        
        if not skip_last:
            self.__zero_orient_joint(self.chain[-1])


    

    def check_coplanar(self, pos_list=[], round_pos=10):
        '''
        This method checks if 4 or more poinst sit on a single plane, and if so defines anormalized vector perpendicular to that plane
        @param pos_list: float[3] list, the position list, cannot be less that 4 positions
        @param round_pos: int, precision of checking, represents the number of decimal digits of dot product and the normal vector
        @return bool
        '''
        
        if not pos_list:
            om1.displayError("Position list not defined")
            return
        
        if len(pos_list) < 4:
            om1.MGlobal.displayError("There has to be at least 4 points")
            return
        
        
        #define first three points as vectors
        vec_0a = om1.MVector(pos_list[0][0], pos_list[0][1], pos_list[0][2])
        vec_0a = om1.MVector(pos_list[1][0], pos_list[1][1], pos_list[1][2])
        vec_0c = om1.MVector(pos_list[2][0], pos_list[2][1], pos_list[2][2])
        
        #define vectors between first three points      
        vec_ab = vec_0a - vec_0a
        vec_ac = vec_0c - vec_0a 
      
        #find cross product (perpendicular vector) to the first three points
        cross_prod =  vec_ac ^ vec_ab

        
        #interate through all the following points 
        #and check if the vector between them and the first point is still perpendicular to the cross product
        for i in range(3,len(pos_list)):
            vec_0x = om1.MVector(pos_list[i][0], pos_list[i][1], pos_list[i][2])
            vec_ax = vec_0x - vec_0a
            dot_prod = vec_ax * cross_prod    
            if (round(dot_prod,round_pos)) != 0.0:
                return False    
        
        self.upVec = cross_prod.normal()      
        return True

       
    def check_collinear(self, pos_list=[], round_pos=10):
        '''
        This method checks if 3 or more poinst sit on a single line
        @param pos_list: float[3] list, the position list, cannot be less that 3 positions
        @param round_pos: int, precision of checking, represents the number of decimal digits of vectors' length and final test equation
        @return bool or None if all the points have same position
        ''' 
        
        if not pos_list:
            om1.displayError("Position list not defined")
            return
        
        if len(pos_list) < 3:
            om1.MGlobal.displayError("There has to be at least 3 points")
            return
        
        
        #find first vector between two points with non-zero lenght
        index = None        
        for i in range(len(pos_list)-1):     
            vec_0a = om1.MVector(pos_list[i][0], pos_list[i][1], pos_list[i][2])
            vec_0a = om1.MVector(pos_list[i+1][0], pos_list[i+1][1], pos_list[i+1][2])
            vec_ab = vec_0a - vec_0a

            if round(vec_ab.length(), round_pos) != 0.0:
                vec_non_0 = om1.MVector(vec_ab)
                index = i
                break
            
        if index == None:
            om1.MGlobal.displayWarning("All the points have same position")
            return 
        
        #interate through all the following points and run a test equation
        for i in range(index+1,len(pos_list)):
            vec_0x = om1.MVector(pos_list[i][0], pos_list[i][1], pos_list[i][2])
            vec_ax = vec_0x - vec_0a
            
            if round(vec_ax.length(), round_pos) == 0.0:
                continue
            
            testEquation = abs((vec_non_0 * vec_ax) / (vec_non_0.length() * vec_ax.length()))
            
            if round(testEquation, round_pos) != 1:
                return False
        
        return True

 
    @staticmethod
    def getVecFromOri(obj=None):
        
        if not obj:
            om2.MGlobal.displayError("Object not defined")
            return
        
        if not pm.objExists(obj):
            om2.MGlobal.displayError("Object '{}' does not exist".format(obj))
            return

        # check if it is a pyNode
        if isinstance(obj, pm.PyNode):
            obj = obj.name()

                   
        #make a object of type MSelectionList and add the obj to it so we can retrieve its 'MObject'.       
        sel_m = om2.MSelectionList()
        sel_m.add(obj)        
        obj_m = sel_m.getDependNode(0)
    

        if (obj_m.hasFn(om2.MFn.kTransform)):       
            #objDagPathM = sel_m.getDagPath(0)
                   
            # get object's pivot in world space and rotation in quaternion
            #objTransformM = om2.MFnTransform(objDagPathM)
            #objPivotM = om2.MVector(objTransformM.rotatePivot(om2.MSpace.kWorld))  
            
            obj_m_tmatrix = om2.MTransformationMatrix(om2.MMatrix(pm.xform(obj, matrix=True, ws=1, q=True)))
            obj_rot_quat = obj_m_tmatrix.rotation(True)
            
            
            #obj_rot_quat = JointChain.getRotationAsQuat(obj)
    
            # create normalized vectors in 3 axes
            x_axis_vec_m = om2.MVector.kXaxisVector
            y_axis_vec_m = om2.MVector.kYaxisVector
            z_axis_vec_m = om2.MVector.kZaxisVector
    
            # rotate the vectors and offset them to match object's transforms
            x_axis_vec_m = x_axis_vec_m.rotateBy(obj_rot_quat)# + objPivotM
            y_axis_vec_m = y_axis_vec_m.rotateBy(obj_rot_quat)# + objPivotM
            z_axis_vec_m = z_axis_vec_m.rotateBy(obj_rot_quat)# + objPivotM
              
            return [x_axis_vec_m, y_axis_vec_m, z_axis_vec_m]
        
        else:
            om2.MGlobal.displayError("Object '{}' is not a transform".format(obj))
            return
            
 
    @staticmethod
    def getRotationAsQuat(obj):
        #make a object of type MSelectionList and add the obj to it so we can retrieve its 'MObject'.
        sel_m = om2.MSelectionList()
        sel_m.add(obj)
        obj_m = sel_m.getDependNode(0)
        
        #check if its a transform        
        if (obj_m.hasFn(om2.MFn.kTransform)):
            xform = om2.MFnTransform(obj_m)
            quat = xform.rotation(om2.MSpace.kWorld, asQuaternion=True) #it needs to work in world space
            #            #targetMTMatrix.rotation(True)
            quat.normalizeIt()
            #py_quat = [quat[x] for x in range(4)]
            #return py_quat 
            return quat
        else:
            om2.MGlobal.displayError("Object '{}' is not a transform".format(obj))
            return



    # def chainLength(self):
    #     '''
    #     This method returns the number of joints in the chain
    #     '''
    #     return len(self.chain)
    #
    #
    # @staticmethod
    # def blendTwoChains(chain1, chain2, resChain, attrHolder, attrName, base_name, side):
    #     '''
    #     TODO: add a check if all the chains have same length (joint number)
    #     This method will blend two provided chains
    #     @param chain1: pyNode[], the first chain you want to blend
    #     @param chain2: pyNode[], the second chain you want to blend
    #     @param resChain: pyNode[], the blended chain
    #     @param attrHolder: pyNode, the node holding the attribute for the blending switch
    #     @param attrName: string, the name of the attribute used to blend
    #     @param base_name: string, the base name used to generate the names
    #     @param side: string, the side used to generate names
    #     @return: dict    
    #     '''
    #
    #     blnTArray = []
    #     blnRArray = []
    #     blnSArray = []
    #     data = {"blendTranslate": blnTArray,
    #             "blendRotate": blnRArray,
    #             "blendScale": blnSArray
    #             }
    #
    #     if attrHolder.hasAttr(attrName) == 0:
    #         attrHolder.addAttr(attrName, at="float", min=0, max=1, dv=0, k=1)
    #
    #
    #     for i,b in enumerate(resChain):
    #         blnT = name_utils.getUniqueName(base_name, side, "BLN")
    #         blnR = name_utils.getUniqueName(base_name, side, "BLN")
    #         blnS = name_utils.getUniqueName(base_name, side, "BLN")
    #
    #         if not blnT or not blnR or not blnS:
    #             return 
    #
    #         blnNodeT = pm.createNode("blendColors", n=blnT)
    #         blnNodeR = pm.createNode("blendColors", n=blnR)
    #         blnNodeS = pm.createNode("blendColors", n=blnS)
    #
    #         chain1[i].t.connect(blnNodeT.color2)
    #         chain2[i].t.connect(blnNodeT.color1)
    #
    #         chain1[i].r.connect(blnNodeR.color2)
    #         chain2[i].r.connect(blnNodeR.color1)
    #
    #         chain1[i].s.connect(blnNodeS.color2)
    #         chain2[i].s.connect(blnNodeS.color1)
    #
    #         blnNodeT.output.connect(b.t)
    #         blnNodeR.output.connect(b.r)
    #         blnNodeS.output.connect(b.s)
    #
    #         blnTArray.append(blnNodeT)
    #         blnRArray.append(blnNodeR)
    #         blnSArray.append(blnNodeS)
    #
    #         attrHolder.attr(attrName).connect(blnNodeT.blender)
    #         attrHolder.attr(attrName).connect(blnNodeR.blender)
    #         attrHolder.attr(attrName).connect(blnNodeS.blender)
    #
    #     return data
            
        
'''
from modules.submodules import jointChain
jc = jointChain.JointChain()
jc.fromList([[x,x,0] for x in range(4)], autoOrient=1)
'''
   
'''
from modules.subModules import jointChain
import pymel.core as pm

pm.select("locator1", "locator2", "locator3", "locator4", "twistLoc")
pm.select("locator5", "locator6", "locator7", "locator8", "twistLoc1")
pos_list = [pm.xform(item, q=1, ws=1, t=1) for item in pm.selected()]

chain = jointChain.JointChain()

chain.test(pos_list)
'''
   
   
'''
from modules.subModules import jointChain
import pymel.core as pm


pm.select(cl=1)
for n in range(32,38):
    pm.select("locator"+str(n), add=1)

pos_list = [pm.xform(item, q=1, ws=1, t=1) for item in pm.selected()]
vecs = jointChain.JointChain.getVecFromOri("locator32")
print (vecs)

chain = jointChain.JointChain()

chain = jointChain.JointChain()
chain.linear_chain(pos_list, aim_axis="+x", upAxis="+y", upVec=vecs[0])
'''
         
        
        
        
        
        
            
            
            
            