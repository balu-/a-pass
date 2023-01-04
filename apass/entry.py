import copy
import uuid as uuidGen
import json

import logging


class Entry():
	""" An decrypted entry - a bunch of values saved with keys and some attributes """

	class Value():
		TYPE_DEFAULT = "default"
		TYPE_PASSWORD = "password"
		TYPE_TOTP = "totp"
		TYPE_USERNAME = "username"
		TYPE_URL = "url"
		LIST_OF_TYPE = [ TYPE_DEFAULT, TYPE_PASSWORD, TYPE_TOTP, TYPE_USERNAME, TYPE_URL ]
		""" Subclass to hold a value of an Entry, and possibliy some attributes of the value (like a type)"""
		def __init__(self, value:str, attr:dict={}, typeOfValue:str=TYPE_DEFAULT):
			self.value = value
			self.attribute = attr
			if typeOfValue in Entry.Value.LIST_OF_TYPE:
				self.type = typeOfValue
			else:
				self.type = Entry.Value.TYPE_DEFAULT

		def __str__(self) -> str:
			return self.value

		def getType(self) -> str:
			return self.type

		def setType(self,typeStr:str) -> str:
			if typeStr in Entry.Value.LIST_OF_TYPE:
				self.type = typeStr
			else:
				raise Exception("unsuported type")

		def getAttribute(self) -> dict:
			return copy.deepcopy(self.attribute)

		def getAttribut(self, key:str):
			return self.attribute[key]

		def setAttribut(self, key:str, value):
			self.attribute[key] = value

		def toDict(self) -> dict:
			return copy.deepcopy(self.__dict__)

	def __init__(self, title:str="", values:dict={}, uuid:str=None):
		self.title = title
		self.values = {}
		for key, value in values.items():
			if type(value) is Entry.Value: 
				self.values[key]=value
			elif type(value) is str:
				self.values[key]= Entry.Value(value)
		if uuid is None:
			uuid = str(uuidGen.uuid4())
		self.uuid = uuid

	def __str__(self) -> str:
		values={}
		for key, value in self.values.items():
			values[key]=str(value)
		return f'{self.__class__.__name__}[{self.title}]({values})'

	def removeValue(self, key:str) -> None:
		"""remove Value by key """
		del self.values[key]

	def addValue(self, key:str, value:'Entry.Value') -> None:
		if key in self.values:
			raise KeyError(str(key))
		self.values[key]=value

	def renameValue(self, oldKey:str, newKey:str) -> None:
		if newKey in self.values:
			raise KeyError(str(newKey))
		self.values[newKey] = self.values[oldKey]
		del self.values[oldKey]

	def getValues(self, ofType:list=Value.LIST_OF_TYPE ) -> dict:
		result={}
		for key, value in self.values.items():
			if value.getType() in ofType:
				result[key]=copy.deepcopy(value) # value
		return result

	def __getitem__(self,attr):
		""" Return Value if exists """
		if attr not in self.values:
			raise KeyError(str(attr))
		return self.values[attr] #copy.deepcopy(self.values[attr]) #copy.deepcopy(str(self.values[attr]))

	def _defaultJsonEncoder(obj):
	    """ Default encoder, encountered must have to_dict method to be serialized.  """
	    if hasattr(obj, "toDict"):
	        return obj.toDict()
	    else:
	        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


	def toJson(self, **kw) -> str:
		return json.dumps(self.__dict__, default=Entry._defaultJsonEncoder, **kw)

	def fromJson(jsonStr:str) -> 'Entry':
		o = json.loads(jsonStr)
		#create Values
		values = {}
		for key, value in o['values'].items():
			values[key] = Entry.Value(value['value'],value.get("attribute",{}), value.get("type", Entry.Value.TYPE_DEFAULT))
		return Entry(o['title'],values,o['uuid'])


