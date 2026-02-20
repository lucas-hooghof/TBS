import sys

class Argument:
    def __init__(self,name: str,flag: str,type: str = "string"):
        self.name = name
        self.flag = flag
        self.type = type


class Instance:
    def __init__(self):
        self.env: list[Argument] = []
        self.dirs = []
        self.errorcode = 0
    def __str__(self):
        return f"ENV: {self.env},Directories: {self.dirs}"
    def AddDirectory(self, dir: str) -> None:
        self.dirs.append(dir)

def CreateInstance(arguments: list[Argument] = []) -> Instance:
    instance: Instance = Instance()

    instance.env.append(Argument("prefix","--prefix","string"))
    instance.env.append(Argument("target","--target","string"))

    for argument in arguments:
        instance.env.append(argument)

    instance.errorcode = 0
    return instance
