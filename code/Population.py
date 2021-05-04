class Individual:
	__fitness=0
	def __init__(self,errarr,vec):
		self.__trainerror=errarr[0]
		self.__validationerror=errarr[1]
		self.__weightvector=vec

	def calculateFitness(self):
		self.__fitness=1/(self.__trainerror+self.__validationerror)
	
	def getfitness(self):
		return self.__fitness
	
	def getweightvector(self):
		return self.__weightvector
	
	def geterrors(self):
		return self.__trainerror,self.__validationerror
