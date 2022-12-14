import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import authenticator.encrypter as encrypter

class Test_encrypt_and_decrypt(unittest.TestCase):


    def test_encrypt_password(self):
        self.assertEqual(encrypter.encrypt_password("Bubbles1206"), "0584beac7f985889050c606a46d8b70b00613ad3f1e70e99eaacf9501bcdf9da8e887369a7e1d5d8cee406e5515233171c2421a18b49e91ea467b947ba4be999")
        self.assertEqual(encrypter.encrypt_password("LightHouse42069"), "0aab975e30ac9352f69fe0e779c11dfcec36cd77926ef071517e5ab43394b3352f5fa4c8135204f7f1073faaea3432975455880e614b1a17e09d4af0918b8a36")


        
if __name__ == "__main__":
   unittest.main()