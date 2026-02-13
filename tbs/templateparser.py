from .Instance import Instance

import glob
import re
import os

class Template:
    def __init__(self,filename: str,templatename:str = ""):
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
        self.file = filename


class TemplateParser:
    def __init__(self,instance: Instance):
        self.instance: Instance = instance
        self.templates: list[Template] = []
    def GetAllTemplatesInDirectories(self):
        for _,dir in enumerate(self.instance.dirs):
            files: list[str] = glob.glob(f"{os.path.abspath(dir)}/*")
            for _,file in enumerate(files):
                if file.endswith(".tbm"):
                    self.templates.append(Template(file))
    def AddTemplate(self,filename):
        self.templates.append(Template(filename))
    
    def ParseTemplate(self,template: Template):
        with open(template.file,"r") as t:
            lines = t.readlines()
            for line in lines:
                if match := re.match(r"C_COMPILER\(([^)]+)\)",line):
                    template.c_compiler = match.group(1)
                    print(f"Found c compiler {template.c_compiler}")
                elif match := re.match(r"CPP_COMPILER\(([^)]+)\)",line):
                    template.cpp_compiler = match.group(1)
                    print(f"Found c++ compiler {template.cpp_compiler}")
                elif match := re.match(r"CHECK_HEADER\(([^)]+)\)",line):
                    template.headersrequired.append(match.group(1))
                    print(f"Found required Header: {match.group(1)}")





        

