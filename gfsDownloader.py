from datetime import datetime

class GFS(object):
	from urllib.request import urlretrieve
	from progress.bar import Bar
	from progress.spinner import Spinner
	
	"""docstring for GFS"""
	def __init__(self, startDate, forecast, resolution):
		self.startDate = startDate
		utcTime = startDate.strftime('%H')
		self.forecast = int(forecast)
		self.resolution = resolution

	def __get(self, url, to):
		self.p = None

		def __update(blocks, bs, size):
			if not self.p:
				if size < 0:

					self.p = GFS.Spinner(to)
				else:

					TOTALSIZE = int(size/1000000)
					self.p = GFS.Bar(to, max=size, fill='=', suffix='{} MB | %(percent).1f%% - %(eta)ds'.format(TOTALSIZE))
			else:
				if size < 0:
					self.p.update()
				else:
					self.p.goto(blocks * bs)

		GFS.urlretrieve(url, to, __update)
		self.p.finish()

	def Download(self):
		link = "http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/"
		fileList = ["gfs.{}{}/gfs.t{}z.pgrb2.0p{}.f{}".format(self.startDate.strftime('%Y%m%d'), 
			                                                                "00", "00", 
			                                                                self.resolution, str(forecasting).zfill(3) )  \
		for forecasting in range(0, self.forecast+1, 3)]

		for fileLink in fileList:
			
			self.__get(link+fileLink, fileLink.split("/")[1])

def cliArguments(cmd=None):
	import argparse as args
	from sys import argv
	from datetime import datetime

	parser = args.ArgumentParser("Loading GFS Downloader arguments...")
	parser.add_argument("-d", "--date",
			                required=True,
			                dest="date",
			                type=lambda d: datetime.strptime(d, '%Y%m%d_%H'),
			                help="Datetime argument must be set example: -d 10-12-2018_10")
	parser.add_argument("-f", "--forecast",
			                required=True,
			                dest="forecastRange",
			                type=str,
			                help="Forecsat range time,  must be set, example: -f 120")
	parser.add_argument("-r", "--resolution",
			                required=True,
			                dest="resolutionModel",
			                type=str,
			                help="Spatial Resolution model, must be set, example: -f 25")
	parser.add_argument("-o", "--outputFile",
			                required=False,
			                type=str,
			                help="path to output the downloaded model files. example: -o /home/user/")

	return parser.parse_args(args=cmd)

def main(cmd=None):
	argsProcess = cliArguments(cmd=cmd)
	return argsProcess.__dict__

if __name__ == '__main__':
	dictArgs = main()
	print(dictArgs['date'], dictArgs['forecastRange'])
	teste = GFS(dictArgs['date'], dictArgs['forecastRange'], 
		        resolution=dictArgs['resolutionModel'])
	teste.Download()

