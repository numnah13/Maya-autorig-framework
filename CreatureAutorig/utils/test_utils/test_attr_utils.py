'''
Created on 20. 4. 2024

@author: mstolarz
'''
import unittest
from utils.attr_utils import get_flat_list, remap_input


class TestGetFlatList(unittest.TestCase):
    def test_get_flat_list(self):
        result_1 = get_flat_list(1,2.4,3)
        self.assertEqual(result_1, [1,2.4,3])
        result_2 = get_flat_list("dog", "cat", "bee")
        self.assertEqual(result_2, ["dog", "cat", "bee"])
        result_3 = get_flat_list("dog")
        self.assertEqual(result_3, ["dog"])
        result_4 = get_flat_list(["dog"])
        self.assertEqual(result_4, ["dog"])
        result_5 = get_flat_list("dog", ["cat", "bee"])
        self.assertEqual(result_5, ["dog", "cat", "bee"])
        result_6 = get_flat_list("dog", ["cat", "bee"])
        self.assertEqual(result_6, ["dog", "cat", "bee"])
        result_7 = get_flat_list("dog", ("cat", [1,2,3], "bee"))
        self.assertEqual(result_7, ["dog", "cat", 1, 2, 3, "bee"])
        result_8 = get_flat_list("dog", {"cat", (1,2,3), "bee"})
        self.assertEqual(result_8, ["dog", {"cat", (1,2,3), "bee"}])
        result_9 = get_flat_list("cat", [1,2,"bee"], "bee")
        self.assertEqual(result_9, ["cat", 1, 2, "bee", "bee"])
        result_10 = get_flat_list({1:"cat", 2:"dog"}, "bee")
        self.assertEqual(result_10, [{1:"cat", 2:"dog"}, "bee"])
        
        print ("Successfully ran test_get_flat_list")
    
    def test_remap_input(self):
        result_1 = remap_input(["a"])
        self.assertEqual(result_1, ["translateX", "translateY", "translateZ",
                                    "rotateX", "rotateY", "rotateZ", 
                                    "scaleX", "scaleY", "scaleZ", 
                                    "visibility"])
        result_2 = remap_input(["s","all"])
        self.assertEqual(result_2, ["translateX", "translateY", "translateZ",
                                    "rotateX", "rotateY", "rotateZ", 
                                    "scaleX", "scaleY", "scaleZ", 
                                    "visibility"])
        result_3 = remap_input(["t","r","s","v"])
        self.assertEqual(result_3, ["translateX", "translateY", "translateZ",
                                    "rotateX", "rotateY", "rotateZ", 
                                    "scaleX", "scaleY", "scaleZ", 
                                    "visibility"])
        result_4 = remap_input(["x", "y", "z"])
        self.assertEqual(result_4, ["translateX", "translateY", "translateZ", 
                                    "rotateX", "rotateY", "rotateZ", 
                                    "scaleX", "scaleY", "scaleZ"])
        result_5 = remap_input(["scale", "visibility"])
        self.assertEqual(result_5, ["scaleX", "scaleY", "scaleZ", "visibility"])
        result_6 = remap_input(["y", "rotate"])
        self.assertEqual(result_6, ["translateY", "rotateX", "rotateY", "rotateZ", 
                                    "scaleY"])
        result_7 = remap_input(["scaleX", "sz"])
        self.assertEqual(result_7, ["scaleX", "scaleZ"])
        result_8 = remap_input(["translate", "rx", "rz"])
        self.assertEqual(result_8, ["translateX", "translateY", "translateZ", 
                                    "rotateX", "rotateZ"])
        
        print ("Successfully ran test_remap_input")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()