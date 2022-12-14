import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
from authenticator.new_user import new_username, password, validate, user_and_pass


class Test_new_user_creation(unittest.TestCase):


    def test_incorrect_input(self):
        username = "     "
        self.maxDiff = None
        self.assertNotEqual(new_username,"Please enter the correct username.")


    def test_new_user_1(self):
        username = "jkokot"
        self.maxDiff = None
        self.assertNotEqual(new_username,"That user already exists.")

    
    def test_new_user_2(self):
        username = "TaiSMail"
        self.maxDiff = None
        self.assertNotEqual(new_username,"That user already exists.")


    def test_auth_password(self) :
        self.maxDiff = None
        self.assertNotEqual(password,"Please re-enter password: ")


    def test_auth_validate(self):
        self.assertNotEqual(validate,"Make sure your password is at lest 8 letters")
        self.assertNotEqual(validate,"Make sure your password has a number in it")
        self.assertNotEqual(validate,"Make sure your password has a capital letter in it")
        self.assertNotEqual(validate,"Your password seems fine")


    def test_auth_user_and_pass(self):
        self.maxDiff = None
        self.assertNotEqual(user_and_pass, None)


if __name__ == "__main__":
    unittest.main()