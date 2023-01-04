import unittest

import json
import time
import shutil, tempfile
import os
import pyrage

#from apass.repo import Repo
from .context import Repo

class TestRepo(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_create_open_onewrite_oneread(self):
        """ Test file functions"""
        e = Repo("secret", fs_path=os.path.join(self.test_dir, '.apass'), createRepo=True)
        self.assertIsInstance(e,Repo, "Should be of class Repo")
        content = "->Test Content<-"
        e._encryptStrToFile("test",content)
        dec_content = e._decryptStrFromFile("test")
        self.assertEqual(dec_content,content, "content should be the same befor and after enc")
        #reopen repo
        f = Repo("secret", fs_path=os.path.join(self.test_dir, '.apass'))
        self.assertIsInstance(e,Repo, "Should be of class Repo")
        dec_content2 = f._decryptStrFromFile("test")
        self.assertEqual(dec_content2,content, "content should be the same befor and after enc")

    def test_read_write(self):
        """ Test file functions"""
        e = Repo("secret", fs_path=os.path.join(self.test_dir, '.apass'), createRepo=True)
        self.assertIsInstance(e,Repo, "Should be of class Repo")
        start = time.time()
        for i in range(100):
            e._encryptStrToFile(str(i),"Test - "+str(i)+" <-")
        write_end = time.time()
        self.assertTrue((write_end - start) < 1, "write should be faster then 1s")
        str_res = {}
        for i in range(100):
            str_res[i] = e._decryptStrFromFile(str(i))
        read_end = time.time()
        self.assertTrue((read_end - write_end) < 1, "read should be faster then 1s")

        self.assertEqual(len(str_res), 100, "Should have 100 items")
        #test values
        for key, value in str_res.items():
            self.assertEqual("Test - "+str(key)+" <-", value, "Key should match expected value")


    def test_persist_load_Entry(self):
        """ Test file functions"""
        with self.assertRaises(Exception) as ex:
            e = Repo("secret", fs_path=os.path.join(self.test_dir, '.apass'))
        self.assertTrue('Could not find existing repo' in str(ex.exception), "should contain attr key in exception")
            #self.assertIsInstance(e,Repo, "Should be of class Repo")

    def test_create_already_existing_repo(self):
        o = Repo("secret", fs_path=os.path.join(self.test_dir, '.apass'), createRepo=True)
        with self.assertRaises(Exception) as ex:
            e = Repo("secret2", fs_path=os.path.join(self.test_dir, '.apass'), createRepo=True)
        self.assertTrue('does already exist' in str(ex.exception), "should contain attr key in exception")
            #self.assertIsInstance(e,Repo, "Should be of class Repo")

    def test_open_with_wrong_PW(self):
        o = Repo("secret", fs_path=os.path.join(self.test_dir, '.apass'), createRepo=True)
        with self.assertRaises(Exception) as ex:
            e = Repo("secret2", fs_path=os.path.join(self.test_dir, '.apass'))
        self.assertTrue('Decryption failed' in str(ex.exception), "should contain attr key in exception")
            #self.assertIsInstance(e,Repo, "Should be of class Repo")

    def test_open_with_wrong_unencrypted_file(self):
        o = Repo("secret", fs_path=os.path.join(self.test_dir, '.apass'), createRepo=True)
        folder = os.path.join(self.test_dir, '.apass', o.STORE)
        with open(os.path.join(folder, "unenc_test_file"), "w") as file:
            file.write("Test___inhalt____unverschluesselt!!!!!")
        with self.assertRaises(pyrage.DecryptError) as ex:
            str_res = o._decryptStrFromFile(os.path.join(o.STORE,"unenc_test_file"))
        self.assertTrue('Header is invalid' in str(ex.exception), "should contain error in exception")



if __name__ == '__main__':
    unittest.main()
