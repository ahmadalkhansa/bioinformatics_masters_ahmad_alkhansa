class Idmanager:
	original:str
	format:str
	def __init__(self, original):
		self.original=original.split("/")[-1] # in case the file is coming from a directory

	def id(self): # the function extracts the id wether there are two dots or one
		if len(self.original.split(".")) == 3:
			original = self.original.split(".")[0]+"."+self.original.split(".")[1]
		else:
			original = self.original.split(".")[0]
		return(original)

	def modify(self, format): #changes the format of the file by just giving the ".fasta" or ".profile"
		return(self.id()+format)
