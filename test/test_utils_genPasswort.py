import unittest

from .context import password
#from apass.repo import Repo
#from apass.entry import Entry


class TestRepoEntry(unittest.TestCase):

    def test_password_generate_simple(self):
        """ test basics """
        for i in range(10):
            pw = password.generate(i)
            self.assertEqual(len(pw),i, " pw should have required length")

    def test_password_generate_alpahabet(self):
        """ test basics """
        for i in range(10):
            pw = password.generate(10, alphabet="abc")
            self.assertEqual(len(pw),10, " pw should have required length")
            self.assertTrue(set("abc").issuperset(pw), " pw should only contain spezified chars")

    def test_password_generate_mustContain(self):
        """ catch the randomness""" 
        pw = password.generate(1, alphabet="abc", mustContain={"a":1})
        self.assertEqual(pw,"a", " pw should have expected value")
        pw = password.generate(1, alphabet="abc", mustContain={"b":1})
        self.assertEqual(pw,"b", " pw should have expected value")
        pw = password.generate(1, alphabet="abc", mustContain={"c":1})
        self.assertEqual(pw,"c", " pw should have expected value")
        pw = password.generate(1, mustContain={"x":1})
        self.assertEqual(pw,"x", " pw should have expected value")


    def test_password_generate_mustContain(self):
        """ catch the randomness""" 
        with self.assertRaises(Exception) as ex:
             pw = password.generate(1, mustContain={"x":2})
        self.assertTrue('mustContain is not fulfillable' in str(ex.exception), "should get exception for not fulfillable condition")
        with self.assertRaises(Exception) as ex:
             pw = password.generate(1, mustContain={"x":1, "a":1})
        self.assertTrue('mustContain is not fulfillable' in str(ex.exception), "should get exception for not fulfillable condition")
        pw = password.generate(2, mustContain={"x":1, "a":1})
        
if __name__ == '__main__':
    unittest.main()
