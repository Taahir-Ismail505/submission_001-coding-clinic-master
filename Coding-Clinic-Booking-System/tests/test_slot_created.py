import sys, os, inspect
from io import StringIO


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import unittest
import test_base
from unittest.mock import patch
import argparse
import functions.calender_api as calender_api
import functions.date_format as df
import datetime
import functions.clinicians.create_clinician_slot as create_clinician_slot
#import auth_interface

service = calender_api.create_auth_service()

# colors = service.colors().get().execute()
d_and_t = df.get_add_to_calender_input("2020-12-09", "11:45")
# now = datetime.datetime.now()
start2 = df.convert_to_RFC_datetime(d_and_t[0], d_and_t[1], d_and_t[2], d_and_t[3][0]-2, d_and_t[3][1])
end = df.convert_to_RFC_datetime(d_and_t[0], d_and_t[1], d_and_t[2], d_and_t[4][0]-2, d_and_t[4][1])


# if auth_interface.check_if_credentials_have_expired():
#         return


class MyTestCase(unittest.TestCase):

    def test_slots_overlap(self):
        global service, start2, end
        
        username = "nmeintje"
        
        a = create_clinician_slot.check_if_slots_overlap(start2, end, service, username)
        self.assertEqual(a, False)
        d_and_t = df.get_add_to_calender_input("2020-12-09", "11:00")
        start2 = df.convert_to_RFC_datetime(d_and_t[0], d_and_t[1], d_and_t[2], d_and_t[3][0]-2, d_and_t[3][1])
        end = df.convert_to_RFC_datetime(d_and_t[0], d_and_t[1], d_and_t[2], d_and_t[4][0]-2, d_and_t[4][1])
        a = create_clinician_slot.check_if_slots_overlap(start2, end, service, username)
        self.assertEqual(a, False)
        
    """
    def test_add_to_calendar(self):
        
        In this unittest we need to mock the value of "overlaps" 
        and set it to False and then True, as well as date and time commandline arguments.
        Namely, 2020-12-09, 11:00. To do this we use patch from the mock library
        
      
    """
    
    # @patch('create_clinician_slot.check_if_slots_overlap', return_value=False)
    # def test_add_to_calendar(self):
    #     global service
    #     username = "nmeintje"  
    #     with unittest.mock.patch('sys.argv', ['create_clinician_slot.py', '2020-12-09', '11:00']): 
    #         with test_base.captured_output() as (out, err):
    #             create_clinician_slot.add_to_calender(service, username)
    #         output = out.getvalue().strip()
    #         self.assertEqual(output,"Your slot has been created...")


if __name__=="__main__":
    unittest.main()