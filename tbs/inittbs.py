import sys

class Instance:
    def __init__(self):
        self.env = {}
        self.templatedirs = []
        self.configure = False
    def getenv(self,key: str):
        return self.env.get(key)

    def __str__(self):
        return f"ENV: {self.env}"
    

def InitilizetbsInstance(cli: list[str] = []) -> Instance:
    inst: Instance = Instance()
    inst.env["Initilized"] = True

    if sys.argv[1] == "configure":
        inst.configure = True
    elif sys.argv[1] == "genconf":
        inst.configure = False

    if cli == None:
        for _,arg in enumerate(sys.argv):
            if arg.startswith("--prefix="):
                prefix = arg.split("=")[1]
                inst.env["prefix"] = prefix
            elif arg.startswith("--target="):
                targetdir = arg.split("=")[1]
                inst.env["target"] = targetdir
    else:
        for _,arg in enumerate(sys.argv):
            if arg.startswith("--prefix="):
                prefix = arg.split("=")[1]
                inst.env["prefix"] = prefix
            elif arg.startswith("--target="):
                targetdir = arg.split("=")[1]
                inst.env["target"] = targetdir
            for _,aarg in enumerate(cli):
                if arg.startswith(aarg):
                    argp = arg.split(aarg)[1]
                    inst.env[aarg.split("--")[1].split("=")[0]]

    return inst
            