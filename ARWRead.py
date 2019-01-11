
class ARW(object):
    """docstring for ARW."""
    def __init__(self, nmlARWFile):
        self.nmlARWFile = nmlARWFile
        self.valueNml = None
        self.maxDom = None

    def __nmlInputDom(self):
        return((((self.valueNml*self.maxDom)+'\n'))[:-1])

    def nmlARWEdit(self, **kwargs):
        with open(self.nmlARWFile, "r") as namelist:
            nmlLines = namelist.readlines()
            for optionOnNamelist in list(kwargs.keys()):
                for idx, line in enumerate(nmlLines):
                    if " "+optionOnNamelist in line:
                        self.valueNml = " "+kwargs[optionOnNamelist]
                        self.maxDom = 1
                        print(nmlLines[idx])
            with open("new.input", "w") as newNamelist:
                newNamelist.writelines(nmlLines)


wps = ARW("namelist.input")
args = {"dx":"15000,",
        "dy":"15000,",
        "start_year":"2018,",
        "max_dom": "1,"}
wps.nmlARWEdit(**args)
