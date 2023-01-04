import unittest

import json
import time
import shutil, tempfile
import os

from .context import Entry
from .context import Repo
#from apass.repo import Repo
#from apass.entry import Entry


class TestRepoEntry(unittest.TestCase):

    SECRET_KEY = "secret"
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        #create repo
        r = Repo(self.SECRET_KEY, fs_path=os.path.join(self.test_dir, '.apass'), createRepo=True)
        self.assertIsInstance(r,Repo, "Should be of class Repo")

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)


    def test_persist_load_Entry(self):
        """ Test file functions"""
        r = Repo(self.SECRET_KEY, fs_path=os.path.join(self.test_dir, '.apass'))
        self.assertIsInstance(r,Repo, "Should be of class Repo")
        e = Entry("test",{"Test":"Test"})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        uuid = str(e.uuid)
        r.saveEntry(e)
        e2 = r.loadEntry(uuid)
        self.assertIsInstance(e2,Entry, "Should be of class Entry")
        self.assertEqual(str(e['Test']), str(e2['Test']), "Values should be equal")
        self.assertEqual(e.uuid, e2.uuid, "Values should be equal")
    
    def test_persist_ls_Entry(self):
        """ Test file functions"""
        r = Repo(self.SECRET_KEY, fs_path=os.path.join(self.test_dir, '.apass'))
        self.assertIsInstance(r,Repo, "Should be of class Repo")
        e = Entry("test",{"Test":"Test"})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        uuid = str(e.uuid)
        r.saveEntry(e)
        lsdict = r.ls()
        self.assertTrue(uuid in lsdict.keys(), " ls should return dict with uuid as a key")
        self.assertEqual(type(lsdict[uuid]),Entry, " ls should return Entry as value of uuid key")
        self.assertEqual(str(lsdict[uuid]),str(e), " string representation should be equal of entrys")

    def test_persist_rmEntry(self):
        """ Test file functions"""
        r = Repo(self.SECRET_KEY, fs_path=os.path.join(self.test_dir, '.apass'))
        self.assertIsInstance(r,Repo, "Should be of class Repo")
        e = Entry("test",{"Test":"Test"})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        uuid = str(e.uuid)
        r.saveEntry(e)
        lsdict = r.ls()
        self.assertTrue(uuid in lsdict.keys(), " ls should return dict with uuid as a key")
        self.assertEqual(type(lsdict[uuid]),Entry, " ls should return Entry as value of uuid key")
        self.assertEqual(str(lsdict[uuid]),str(e), " string representation should be equal of entrys")
        r.deleteEntry(uuid)
        lsdict = r.ls()
        self.assertFalse(uuid in lsdict.keys(), " ls should no longer return dict with uuid as a key")


        
if __name__ == '__main__':
    unittest.main()
