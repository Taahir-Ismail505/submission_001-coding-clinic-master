import unittest
import os.path
from os import path

class MyTestCase(unittest.TestCase):

    
        
    
    def test_unittest_exist(self):
            
            self.assertTrue(path.exists("token.pickle"), "wtc-clinic login")

if __name__=="__main__":
    unittest.main()