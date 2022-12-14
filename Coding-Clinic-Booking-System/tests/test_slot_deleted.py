import sys, os, inspect
from io import StringIO


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import test_base
from unittest.mock import patch
import calender_api
import date_format as df
import datetime
import functions.clinicians.delete_clinician_slot
#import auth_interface

service = calender_api.create_auth_service()

class MyTestCase(unittest.TestCase):
    def test_asfa(self):
        

if __name__=="__main__":
    unittest.main()