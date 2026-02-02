from .inittbs import Instance

def AddTemplateDirectory(instance: Instance,directory: str):
    instance.templatedirs.append(directory)


    