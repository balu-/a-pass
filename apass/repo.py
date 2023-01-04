
import logging
logging.basicConfig(level=logging.DEBUG)

import json 

import os
from pyrage import passphrase as passphrase_crypt
from pyrage import x25519
from pyrage import encrypt, decrypt

import time

#from apass.entry import Entry
from .entry import Entry

class Repo():

	def _checkFolder(self, path) -> bool:
		return (os.path.isdir(self.fs_path) and os.path.isdir(os.path.join(self.fs_path, self.STORE)) and
			os.path.exists(os.path.join(self.fs_path, 'identity')))

	def _setupRepository(self, passphrase:str) -> None:
		#make sure folder does not exist
		if self._checkFolder(self.fs_path):
			raise Exception(f"Folder {self.fs_path} does already exist")
		#create folder
		os.mkdir(self.fs_path,self.MODE)
		#create store 
		os.mkdir(os.path.join( self.fs_path, self.STORE),self.MODE)
		#create Idenity
		self.ident = x25519.Identity.generate()
		# crypt the key
		encrypted = passphrase_crypt.encrypt(bytes(str(self.ident),"utf-8"), passphrase)
		with open(os.path.join( self.fs_path, self.IDENTITIES), "wb") as file:
			# Writing data to a file
			file.write(encrypted)

		self.recipients.append( self.ident.to_public() )
		recipientsStrList = []
		for r in self.recipients:
			recipientsStrList.append(str(self.ident.to_public()))
		self._encryptStrToFile(self.RECIPIENTS, json.dumps(recipientsStrList))

		#decrypted = passphrase.decrypt(encrypted, "my extremely secure password")
	def _openRepository(self, passphrase:str) -> None:
		with open(os.path.join(self.fs_path, self.IDENTITIES), "rb") as f:
			self.ident = x25519.Identity.from_str( passphrase_crypt.decrypt(f.read(), passphrase).decode('utf-8') )

		file_str = self._decryptStrFromFile(self.RECIPIENTS)
		recipientsStrList = json.loads(file_str)
		for r in recipientsStrList:
			self.recipients.append(x25519.Recipient.from_str( r ))

	def _decryptStrFromFile(self, path:str) -> str:
		with open(os.path.join(self.fs_path, path), "rb") as f: 
			res = decrypt(f.read(), [ self.ident ]).decode('utf-8') 
			return res

	def _encryptStrToFile(self, path:str, content:str, overwrite:bool=False) -> None:
		with open(os.path.join( self.fs_path, path), "wb") as file:
			enc_content = encrypt(bytes(content,"utf-8"), self.recipients )
			file.write(enc_content)

	def __init__(self,passphrase:str, fs_path:str=os.path.join(os.path.expanduser( '~' ), ".apass"), createRepo:bool=False, cache:bool=True):
		self.ident = None
		self.recipients = []
		self.fs_path= fs_path
		self.IDENTITIES="identity"
		self.RECIPIENTS="recipients"
		self.STORE="store/"
		self.MODE=0o700
		folderExists = self._checkFolder(self.fs_path)
		if createRepo:
			self._setupRepository(passphrase)
		elif not createRepo and folderExists:
			self._openRepository(passphrase)
		elif not createRepo and not folderExists:
			raise Exception("Could not find existing repo")

		self.cache = None
		if cache:
			self.cache = {}
			for f in [ f for f in os.listdir(os.path.join(self.fs_path, self.STORE)) if os.path.isfile(os.path.join(os.path.join(self.fs_path, self.STORE),f))]:
				self.cache[f]=self.loadEntry(f)

	def ls(self)->dict[str,Entry]:
		if self.cache is not None:
			ret = self.cache
		else:
			ret = {}
			for f in [ f for f in os.listdir(os.path.join(self.fs_path, self.STORE)) if os.path.isfile(os.path.join(os.path.join(self.fs_path, self.STORE),f))]:
				ret[f]=self.loadEntry(f)
		return ret


	def saveEntry(self, entry:Entry) -> None:
		""" save Entry object to file in this repository"""
		self._encryptStrToFile( os.path.join(self.fs_path, self.STORE, str(entry.uuid)), entry.toJson())
		if self.cache is not None:
			self.cache[str(entry.uuid)] = entry

	def deleteEntry(self, uuid:str):
		os.remove(os.path.join(self.fs_path, self.STORE, uuid))
		if self.cache is not None:
			del self.cache[uuid]

	def loadEntry(self, uuid:str) -> Entry:
		entryStr = self._decryptStrFromFile( os.path.join(self.fs_path, self.STORE, str(uuid)))
		return Entry.fromJson(entryStr)	 

