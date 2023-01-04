import unittest

import json

from .context import Entry
#from apass.entry import Entry

class TestEntry(unittest.TestCase):

    def test_create(self):
        e = Entry("test",{"Test":"Test"})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        #self.assertEqual(, 6, "Should be 6")

    def test_double_create(self):
        e = Entry("test",{"Test":"Test"})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        e2 = Entry("test2",{"Test":"Test"})
        self.assertIsInstance(e,Entry, "Should be of class Entry")
        self.assertNotEqual(e.uuid, e2.uuid, "UUIDs should be different")
        #self.assertEqual(, 6, "Should be 6")

    def test_str(self):
        e = Entry("test",{"Test":"Test"})
        self.assertEqual(str(e), "Entry[test]({'Test': 'Test'})", "produce excpected string representation")
    
    def test_getValues(self):
        e = Entry("test",{"Test":"Test"})
        values = e.getValues()
        self.assertEqual(str(values["Test"]),"Test", "should get the same values")
        self.assertNotEqual(id(values),id(e.getValues()), "getValues should return a new instance every call" )

    def test_removeValue(self):
        e = Entry("test",{"Test":"Test"})
        e.removeValue("Test") #remove key Test & Value
        self.assertEqual(e.getValues(),{}, "values should be empty")

    def test_addValues(self):
        e = Entry("test",{})
        e.addValue("Test",Entry.Value("Test"))
        self.assertEqual(str(e["Test"]),"Test", "should get the same values")
        with self.assertRaises(KeyError) as ex:
            e.addValue("Test","")
        self.assertTrue('Test' in str(ex.exception), "should get exception for adding already existing key; contain attr key in exception")
    
    def test_getAttr(self):
        e = Entry("test",{"Test":"Test"})
        self.assertEqual(str(e['Test']), "Test", "accessing values should be easy& direct")
        with self.assertRaises(KeyError) as ex:
            val = e['blub']
        self.assertTrue('blub' in str(ex.exception), "should contain attr key in exception")

    def test_encode_as_json(self):
        title = "ti t_le"
        e = Entry(title,{"key":"val"})
        json = e.toJson()
        #check for json parts
        for part in ['"title": "'+str(title)+'"', 
                     '"values": {', 
                     '"value": "val"' ]:
            self.assertIn(part,json, "string should be in json encoding")

    def test_decode_from_json(self):
        json = '{"title": "ti t_le", "values": {"key": {"value": "val", "attribute": {}}}, "uuid": "afeaa543-74aa-4072-ac80-d2f35f7f97d9"}'
        e2 = Entry.fromJson(json)
        for key, value in { 'key': 'val'}.items():
            self.assertEqual(str(e2[key]), value, "value should be the same")
        self.assertEqual(e2.uuid, "afeaa543-74aa-4072-ac80-d2f35f7f97d9", "value should be the same")
        

    def test_json_roundtrip(self):
        title = "ti t_le"
        e = Entry(title,{"key":"val123"})
        json = e.toJson()
        e2 = Entry.fromJson(json)
        self.assertEqual(str(e['key']), str(e2['key']), "value should be the same")
        self.assertEqual(e.uuid, e2.uuid, "value should be the same")

    def test_json_roundtrip_attr(self):
        title = "ti t_le"
        e = Entry(title,{"key": Entry.Value("test", {"myattr": "myattrvalue"})})
        json = e.toJson()
        e2 = Entry.fromJson(json)
        self.assertEqual(str(e['key']), str(e2['key']), "value should be the same")
        self.assertEqual(e.uuid, e2.uuid, "value should be the same")
        self.assertEqual(e.title, e2.title, "value should be the same")
        self.assertEqual(e['key'].getAttribute(), e2['key'].getAttribute(), "attribute should be the same")

    def test_json_roundtrip_type(self):
        title = "ti t_le"
        e = Entry(title,{"key": Entry.Value("test")})
        e['key'].setType(Entry.Value.TYPE_PASSWORD)
        json = e.toJson()
        e2 = Entry.fromJson(json)
        self.assertEqual(str(e['key']), str(e2['key']), "value should be the same")
        self.assertEqual(e.uuid, e2.uuid, "value should be the same")
        self.assertEqual(e.title, e2.title, "value should be the same")
        self.assertEqual(e['key'].getType(), e2['key'].getType(), "attribute should be the same")


if __name__ == '__main__':
    unittest.main()
