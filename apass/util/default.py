

from apass.entry import Entry 

def defaultEntry():
	return Entry("", { "Username" : Entry.Value("", typeOfValue=Entry.Value.TYPE_USERNAME), 
					   "Password" : Entry.Value("", typeOfValue=Entry.Value.TYPE_PASSWORD), 
					   "Url"      : Entry.Value("", typeOfValue=Entry.Value.TYPE_URL)})