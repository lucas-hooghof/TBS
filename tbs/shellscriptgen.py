from .templateparser import Template,TemplateParser
from .Instance import Instance

import os
import textwrap

class ScriptGen:
    RED = "\033[0;31m"
    NORMAL = "\033[0m"
    DEFINES = ""
    def __init__(self,instance: Instance,templateparser: TemplateParser,root: str):
        self.instance = instance
        self.templateparser = templateparser

        self.scriptloc = f"{root}/configure.sh"
        self.scriptfile = open(self.scriptloc,"w+")

        self.scriptfile.write("#Parsing Arguments\n")
        self.scriptfile.writelines(self.genargparsecode())
        self.scriptfile.write('\n')

        self.scriptfile.write("#Makefile stuff")
        self.scriptfile.write("OPT_FUNCTIONS_PRESENT=""\n")

        

        for template in self.templateparser.templates:
            self.checkforapp(template.c_compiler)
            self.checkforapp(template.cpp_compiler)

            for header in template.headersrequired:
                self.checkforheader(header)
            
            for functions in template.functionsrequired:
                print(functions)
                self.checkforfunctionreq(functions[0],functions[1],functions[2])
                        
            for functions in template.functionsoptional:
                print(functions)
                self.checkforfunctionopt(functions[0],functions[1],functions[2])

        self.scriptfile.write("echo $OPT_FUNCTIONS_PRESENT\n")

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
    def genargparsecode(self):
        lines = []

        # Variable declarations
        for arg in self.instance.env:
            if arg.type == "bool":
                lines.append(f'{arg.name}=false')
            elif arg.type == "int":
                lines.append(f'{arg.name}=0')
            else:  # string
                lines.append(f'{arg.name}=""')

        lines.append("")
        lines.append('for arg in "$@"; do')
        lines.append('    case $arg in')

        for arg in self.instance.env:

            # Boolean flag (no value, just set to true)
            if arg.type == "bool":
                lines.append(f'        {arg.flag})')
                lines.append(f'            {arg.name}=true')
                lines.append('            ;;')

            # Integer flag
            elif arg.type == "int":
                lines.append(f'        {arg.flag}=*)')
                lines.append(f'            {arg.name}="${{arg#*=}}"')
                lines.append(f'            if ! [[ "${arg.name}" =~ ^[0-9]+$ ]]; then')
                lines.append(f'                echo "{self.RED}Error: {arg.flag} requires integer{self.NORMAL}"')
                lines.append('                exit 1')
                lines.append('            fi')
                lines.append('            ;;')

            # String flag
            else:
                lines.append(f'        {arg.flag}=*)')
                lines.append(f'            {arg.name}="${{arg#*=}}"')
                lines.append('            ;;')

        # Unknown flag handler
        lines.append('        *)')
        lines.append(f'            echo "{self.RED}Unknown option: $arg{self.NORMAL}"')
        lines.append('            exit 1')
        lines.append('            ;;')

        lines.append('    esac')
        lines.append('done')

        return "\n".join(lines)
    
    def checkforfunctionreq(self,function,header,lib):
        if function == "": return 
        checkstr = textwrap.dedent(f"""\
                                    echo -n "Checking for {function} ..... "
                                    echo '#include <{header}>
                                          int main() {{void *p = (void*){function}; return 0;}}' | gcc -x c - -o /dev/null {f"-l{lib}" if lib != "" else ""} > /dev/null 2>&1
                                    if [ $? -eq 0 ]; then
                                        echo "found {function}"
                                    else
                                        echo '{self.RED}{function} not found unable to compile{self.NORMAL}'
                                    fi\n""")
        self.scriptfile.write(checkstr)

    def checkforfunctionopt(self,function,header,lib):
        if function == "": return 
        checkstr = textwrap.dedent(f"""\
                                    echo -n "Checking for {function} ..... "
                                    echo '#include <{header}>
                                          int main() {{void *p = (void*){function}; return 0;}}' | gcc -x c - -o /dev/null {f"-l{lib}" if lib != "" else ""} > /dev/null 2>&1
                                    if [ $? -eq 0 ]; then
                                        echo "found {function}"
                                        OPT_FUNCTIONS_PRESENT+="-DHAVE_{function.upper()}"
                                    else
                                        echo "{function} not found"
                                    fi\n""")
        self.scriptfile.write(checkstr)

    #TODO: Inplement function to create the code for resolving the files
    #TODO: Inplement code to create a base makefile per template directory
    #TODO: Inplement code to resolve the dependecies
    #TODO: Inplement function to resolve the makefile env's in conf script
    