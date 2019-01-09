

class WPS(object):
	"""docstring for WPS"""
	def __init__(self, nmlWPSFile):
		#self.startDate = startDate
		self.nmlWPSFile = nmlWPSFile
		self.valueNml = None
		self.maxDom = None

	
	def __nmlInputDom(self):
		return((((self.valueNml*self.maxDom)+'\n'))[:-1])

	def nmlWPSEdit(self, **kwargs):
		with open(self.nmlWPSFile, "r") as namelist:
			nmlLines = namelist.readlines()
			for keyNml in list(kwargs.keys()):
				for idx, line in enumerate(nmlLines):
					if keyNml in line:
						self.valueNml = kwargs[keyNml]
						if keyNml is "start_date":
							self.maxDom = 2
							nmlLines[idx] = ' ' + keyNml + ' = ' + "{0}".format(self.__nmlInputDom()) + "\n"
							#print(nmlLines[idx])
						else:
							self.maxDom = 1
							nmlLines[idx] = ' ' + keyNml + ' = ' + "{0}".format(self.__nmlInputDom()) + "\n"
							#print(nmlLines[idx])
						
			with open("new.wps", "w") as newNamelist:
				newNamelist.writelines(nmlLines)
	


	def runGeogrid(self):
		pass

	def plotGridWRF(self):
		pass

	def runMetgrid(self):
		pass


wps = WPS("namelist.wps")
args = {"dx": "15000, ",
        "dy": "15000, ",
        "start_date": "'2006-08-16_12:00:00',",
        "end_date": "'2006-08-16_18:00:00',",
        "max_dom": "1"}
wps.nmlWPSEdit(**args)