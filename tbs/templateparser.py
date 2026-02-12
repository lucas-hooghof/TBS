from .Instance import Instance

class Template:
    def __init__(self,templatename:str = ""):
        self.headersdirs = []
        self.cfiles: list[str] = []
        self.cppfiles: list[str] = []
        self.libraries: list[str] = []
        self.functionsrequired: list[str] = []
        self.functionsoptional: list[str] = []
        self.headersrequired: list[str] = []
        self.templatedependencies: list[Template] = []

        self.outputname: str = ""
        self.c_compiler: str = ""
        self.cpp_compiler: str = ""
        self.defines: str = ""

        self.templatename = templatename

class TemplateParser:
    def __init__(self,instance: Instance):
        self.instance: Instance = instance
        self.templates: list[Template] = []

