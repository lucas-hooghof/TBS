from .templateparser import Template,TemplateParser
from .Instance import Instance

import os
import textwrap

class ScriptGen:
    RED = "\033[0;31m"
    NORMAL = "\033[0m"
    def __init__(self,instance: Instance,templateparser: TemplateParser,root: str):
        self.instance = instance
        self.templateparser = templateparser

        self.scriptloc = f"{root}/configure.sh"
        self.scriptfile = open(self.scriptloc,"w+")

        for template in self.templateparser.templates:
            self.checkforapp(template.c_compiler)
            self.checkforapp(template.cpp_compiler)

            for header in template.headersrequired:
                self.checkforheader(header)

        os.system(f"chmod +x {self.scriptloc}")

    def checkforapp(self,app):
        if app == "": return
        checkstr = textwrap.dedent(f"""\
                    echo -n 'checking for {app}...... '\n
                    if command -v {app} >/dev/null 2>&1; then
                        echo 'found {app}'
                    else
                        echo '{self.RED}{app} not found please install{self.NORMAL}'
                    fi\n\n""")
        self.scriptfile.write(checkstr)
    def checkforheader(self,header):
        if header == "": return
        checkstr = textwrap.dedent(f"""\
                    echo -n 'checking for {header}...... '\n
                    echo '#include <{header}>
                          int main() {{return 0;}}' | gcc -x c - -o /dev/null >/dev/null 2>&1
                    if [ $? -eq 0 ]; then
                        echo "found {header}"
                    else
                        echo '{self.RED}{header} not found unable to compile{self.NORMAL}'
                    fi\n\n            
                    """)
        self.scriptfile.write(checkstr)

    #TODO: Inplement check for function
    #TODO: Inplement function to create the code for resolving the files
    #TODO: Inplement code to create a base makefile per template directory
    #TODO: Inplement code to resolve the dependecies
    #TODO: Inplement function to resolve the makefile env's in conf script
    