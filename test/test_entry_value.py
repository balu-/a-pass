import unittest

import json

from .context import Entry
#from apass.entry import Entry

class TestEntry(unittest.TestCase):

    def test_create_addValue(self):
        e = Entry("test")
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        with self.assertRaises(KeyError) as ex:
            value = e["Test"]
        self.assertTrue('Test' in str(ex.exception), "should get exception for adding already existing key; contain attr key in exception")
        value = Entry.Value("geheim")
        e.addValue("Test",value)
        self.assertEqual('geheim',str(e["Test"]), "value should be accessible")

    def test_create_renameValue(self):
        e = Entry("test", {"val1": Entry.Value("geheim", typeOfValue=Entry.Value.TYPE_PASSWORD)})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        e.renameValue('val1', 'val2')
        self.assertEqual('geheim',str(e["val2"]), "value should be accessible")
        with self.assertRaises(KeyError) as ex:
            value = e["val1"]
        self.assertTrue('val1' in str(ex.exception), "should get exception for adding already existing key; contain attr key in exception")

    def test_ValueType(self):
        e = Entry("test", {"val1": Entry.Value("geheim", typeOfValue=Entry.Value.TYPE_PASSWORD)})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        typeOfV = e["val1"].getType()
        self.assertEqual(typeOfV,Entry.Value.TYPE_PASSWORD, "type should be the one it was initialized with")

    def test_getValueType(self):
        e = Entry("test", {"val1": Entry.Value("geheim", typeOfValue=Entry.Value.TYPE_PASSWORD), "val2": Entry.Value("user", typeOfValue=Entry.Value.TYPE_USERNAME)})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        vals = e.getValues()
        self.assertIsInstance(vals,dict, "Should be of class dict")
        self.assertEqual(vals['val1'].getType(), Entry.Value.TYPE_PASSWORD, "type should be the one it was initialized with")
        self.assertEqual(vals['val2'].getType(), Entry.Value.TYPE_USERNAME, "type should be the one it was initialized with")
        self.assertEqual(len(vals), 2 )
        val1 = e.getValues(ofType=[Entry.Value.TYPE_PASSWORD])
        self.assertIsInstance(val1,dict, "Should be of class dict")
        self.assertEqual(len(val1), 1 )
        self.assertEqual(val1['val1'].getType(), Entry.Value.TYPE_PASSWORD, "type should be the one it was initialized with")
        #typeOfV = e["val1"].getType()
        #self.assertEqual(typeOfV,Entry.Value.TYPE_PASSWORD, "type should be the one it was initialized with")


    def test_jsonValueType(self):
        e = Entry("test", {"val1": Entry.Value("geheim", typeOfValue=Entry.Value.TYPE_PASSWORD)})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        json = e.toJson()
        e2 = Entry.fromJson(json)
        typeOfV = e2["val1"].getType()
        self.assertEqual(typeOfV,Entry.Value.TYPE_PASSWORD, "type should be the one it was initialized with")


if __name__ == '__main__':
    unittest.main()
