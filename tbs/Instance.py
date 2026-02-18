import sys

class Instance:
    def __init__(self):
        self.env = []
        self.dirs = []
        self.errorcode = 0
    def __str__(self):
        return f"ENV: {self.env},Directories: {self.dirs}"
    def AddDirectory(self, dir: str) -> None:
        self.dirs.append(dir)

def CreateInstance(additionalenvs: list[str] = []) -> Instance:
    instance: Instance = Instance()
    instance.env.append("prefix")
    instance.env.append("target")

    for env in additionalenvs:
        instance.env.append(env)

    instance.errorcode = 0
    return instance
