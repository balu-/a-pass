import logging
logging.basicConfig(level=logging.DEBUG)


import secrets
import string


def generate(password_length:int, alphabet:str = string.ascii_letters+string.digits+"!\"#$%&'()*+,-./:;<=>?@[\\]^_{|}~", mustContain:dict[str, int] = {}) -> str:
	""" Generates a passwort of length "len" from the given "alphabet"
		that contains int chars from str alphabet of mustContain dict (bsp. {"a":1} -> contains at least 1 'a')"""
	#check if mustcontain is in alphabet
	sumMustContain = 0
	for char, count in mustContain.items():
		sumMustContain+=count
		count = sum(c in alphabet for c in char)
		if count == 0:
			raise Exception("mustContain is not fulfillable")
		elif count < len(char):
			logging.warning("mustContain has parts that are not in alphabet")
	if sumMustContain > password_length:
		raise Exception("mustContain is not fulfillable")

	password = ''
	while True:
		password = ''
		for i in range(password_length):
			password += ''.join(secrets.choice(alphabet))
		#check if pw matches expectation
		reject = False
		for char, count in mustContain.items():
			if sum(c in char for c in password) < count:
				reject = True

		if not reject:
			break
	return password


if __name__ == '__main__':
	for i in range(3):
		print(f"{i} - {genPasswort(4, mustContain={'aA':2, 'pP':1, 'sS':2})}") #,mustContain={'aö':3})}")


