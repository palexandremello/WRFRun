class WPS(object):
	"""docstring for WPS"""
	def __init__(self, nmlWPSFile, WPSPath):
		#self.startDate = startDate
		self.nmlWPSFile = nmlWPSFile
		self.valueNml = None
		self.maxDom = None
		self.WPSPath = WPSPath

	def __nmlInputDom(self):
		return((((self.valueNml*self.maxDom)+'\n'))[:-1])

	def nmlWPSEdit(self, **kwargs):
		import shutil
		shutil.copy(self.WPSPath+self.nmlWPSFile,
		             self.WPSPath+self.nmlWPSFile+'.bkp')

		with open(self.WPSPath+self.nmlWPSFile, "r") as namelist:
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
		with open(self.WPSPath+"namelist.wps", "w") as newNamelist:
			newNamelist.writelines(nmlLines)

	def runGeogrid(self):
		import os
		os.chdir(self.WPSPath)
		os.system("./geogrid.exe")
		geogridLog = open('geogrid.log').readlines()

		if "Successful completion" in geogridLog[-1]:
			print (">>>>>>>> {} has completed successfully. <<<<<<<<".format('geogrid'))
		else:
			print ('!!!!!!!! geogrid has failed. Exiting... !!!!!!!!')
		pass

	def runUngrib(self, path):
		import os
		os.chdir(self.WPSPath)
		os.system("./link_grib.csh {}gfs*".format(path))
		os.system("ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable")
		os.system("./ungrib.exe")
		os.system("rm -rf GRIBFILE*")
		geogridLog = open('geogrid.log').readlines()

		if "Successful completion" in geogridLog[-1]:
			print (">>>>>>>> {} has completed successfully. <<<<<<<<".format('geogrid'))
		else:
			print ('!!!!!!!! geogrid has failed. Exiting... !!!!!!!!')
		pass

	def runMetgrid(self):
		import os
		os.chdir(self.WPSPath)
		os.system("./metgrid.exe")
		os.system("rm -rf FILE:*")
		geogridLog = open('geogrid.log').readlines()

		if "Successful completion" in geogridLog[-1]:
			print (">>>>>>>> {} has completed successfully. <<<<<<<<".format('geogrid'))
		else:
			print ('!!!!!!!! geogrid has failed. Exiting... !!!!!!!!')
		pass


import gfsDownloader

DataModel = gfsDownloader.GFS("10-01-2019_00",
                              "24", "/home/paulo/DADOS/",
							  "50")
#DataModel.Download()
wps = WPS("namelist.wps",
          "/home/paulo/PythonProjects/WRF/WPS/")

args = {"dx": "15000, ",
        "dy": "15000, ",
        "start_date": "'2019-01-10_00:00:00',",
        "end_date": "'2019-01-11_00:00:00',",
        "max_dom": "1",
		"geog_data_path": " '/home/paulo/PythonProjects/WRF/WPS_GEOG' "}

wps.nmlWPSEdit(**args)
wps.runGeogrid()
wps.runUngrib(DataModel.path)
wps.runMetgrid()
