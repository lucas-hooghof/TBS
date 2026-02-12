import sys

class Instance:
    def __init__(self):
        self.env = {}
        self.dirs = []
        self.errorcode = 0
    def __str__(self):
        return f"ENV: {self.env},Directories: {self.dirs}"
    def AddDirectory(self, dir: str) -> None:
        self.dirs.append(dir)

def CreateInstance(additionalenvs: list[str] = []) -> Instance:
    instance: Instance = Instance()

    for _,arg in enumerate(sys.argv):
        if arg.__contains__("--prefix="):
            prefix = arg.split("=")
            instance.env["prefix"] = prefix[1]
        elif arg.__contains__("--target="):
            target = arg.split("=")
            instance.env["target"] = target[1]
        else:
            for _,envs in enumerate(additionalenvs):
                if arg.__contains__(envs):
                    env = arg.split("=")
                    instance.env[envs] = env[1]

    instance.errorcode = 0
    return instance
