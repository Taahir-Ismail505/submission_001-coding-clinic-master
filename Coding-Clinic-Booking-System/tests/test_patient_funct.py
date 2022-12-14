import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from functions.patients import signup_to_patient_slot
from functions.patients import delete_patient_slot
#####
update_slot_with_deleted_patient = delete_patient_slot.update_slot_with_deleted_patient
#####
delete_patient_slot= delete_patient_slot.delete_patient_slot 
#####
update_slot_with_patient = signup_to_patient_slot.update_slot_with_patient
#####
add_patient_slot_to_calender = signup_to_patient_slot.add_patient_slot_to_calender

import unittest


class MyTestCase(unittest.TestCase):
#############################################################################################
                                #Test for Functions.patients 
                                
    def test_update_slot_with_patient(self):
        self.maxDiff = None
        self.assertNotEqual(update_slot_with_patient,"The slot you tried signing up for is already taken. Please choose another slot.")
        
        
    def  test_add_patient(self):
        self.maxDiff = None
        self.assertNotEqual(add_patient_slot_to_calender,"Please enter a valid ID.")


    def test_delete_clinitian_slot(self):
        self.maxDiff = None
        self.assertNotEqual(delete_patient_slot,"There are currently no available slots to delete.")


    def test_update_slot_with_deleted_patient(self):
        self.maxDiff =None
        self.assertNotEqual(update_slot_with_deleted_patient,None)


if __name__ == "__main__":
   unittest.main()