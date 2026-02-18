from .Instance import Instance
from pathlib import Path

import glob
import re
import os


class Template:
    def __init__(self, filename: str, templatename: str = ""):
        self.headersdirs = []

        # Resolved files (filled later by configure stage)
        self.cfiles: list[str] = []
        self.cppfiles: list[str] = []

        # NEW: store FILES(...) patterns
        self.file_patterns: list[str] = []

        self.libraries: list[str] = []
        self.functionsrequired: list[tuple[str, str, str]] = []
        self.functionsoptional: list[tuple[str, str, str]] = []
        self.headersrequired: list[str] = []
        self.templatedependencies: list["Template"] = []

        self.outputname: str = ""
        self.c_compiler: str = ""
        self.cpp_compiler: str = ""
        self.defines: str = ""

        self.templatename = templatename
        self.file = filename

    def __str__(self):

        name = self.templatename or Path(self.file).stem

        lines = [
            f"╔═══ Template: {name} ═══",
            f"║ File: {self.file}",
            f"║ Output: {self.outputname or 'Not set'}",
            f"║",
            f"║ Compilers:",
            f"║   C:   {self.c_compiler or 'gcc'}",
            f"║   C++: {self.cpp_compiler or 'g++'}",
            f"║",
        ]

        # Show file patterns (NEW)
        lines.append(f"║ File Patterns: {len(self.file_patterns)}")
        if self.file_patterns:
            patterns_preview = ', '.join(self.file_patterns[:5])
            if len(self.file_patterns) > 5:
                patterns_preview += " ..."
            lines.append(f"║   {patterns_preview}")

        lines.append(f"║")

        # Source files (resolved later)
        total_sources = len(self.cfiles) + len(self.cppfiles)
        lines.append(f"║ Source Files: ({total_sources} total)")
        if self.cfiles:
            files_preview = ', '.join(self.cfiles[:3])
            if len(self.cfiles) > 3:
                files_preview += " ..."
            lines.append(f"║   C:   {files_preview}")
        if self.cppfiles:
            files_preview = ', '.join(self.cppfiles[:3])
            if len(self.cppfiles) > 3:
                files_preview += " ..."
            lines.append(f"║   C++: {files_preview}")

        lines.append(f"║")

        # Headers
        lines.append(f"║ Headers Required: {len(self.headersrequired)}")
        if self.headersrequired:
            headers_preview = ', '.join(self.headersrequired[:5])
            if len(self.headersrequired) > 5:
                headers_preview += " ..."
            lines.append(f"║   {headers_preview}")

        lines.append(f"║")

        # Functions
        lines.append(f"║ Functions:")
        lines.append(f"║   Required: {len(self.functionsrequired)}")
        for func, header, libs in self.functionsrequired:
            libs_str = f" {libs}" if libs else ""
            lines.append(f"║     - {func} ({header}){libs_str}")

        lines.append(f"║   Optional: {len(self.functionsoptional)}")
        for func, header, libs in self.functionsoptional:
            libs_str = f" {libs}" if libs else ""
            lines.append(f"║     - {func} ({header}){libs_str}")

        # Libraries
        if self.libraries:
            lines.append(f"║")
            lines.append(f"║ Libraries: {', '.join(self.libraries)}")

        # Dependencies
        if self.templatedependencies:
            lines.append(f"║")
            lines.append(f"║ Dependencies: {len(self.templatedependencies)}")
            for dep in self.templatedependencies:
                dep_name = dep.templatename or Path(dep.file).stem
                lines.append(f"║   - {dep_name}")

        lines.append(f"╚{'═' * (len(lines[0]) - 1)}")

        return '\n'.join(lines)


class TemplateParser:
    def __init__(self, instance: Instance):
        self.instance: Instance = instance
        self.templates: list[Template] = []

    def GetAllTemplatesInDirectories(self):
        for dir in self.instance.dirs:
            files: list[str] = glob.glob(f"{os.path.abspath(dir)}/*")
            for file in files:
                if file.endswith(".tbm"):
                    self.templates.append(Template(file))

    def AddTemplate(self, filename):
        self.templates.append(Template(filename))

    def ParseTemplates(self):
        for template in self.templates:
            self.ParseTemplate(template)
    
    def __str__(self):
        ostr = ""
        for template in self.templates:
            ostr += template.__str__()
            ostr += "\n"

    def ParseTemplate(self, template: Template):
        with open(template.file, "r") as t:
            lines = t.readlines()

        for line in lines:

            line = line.strip()

            if match := re.match(r"C_COMPILER\(([^)]+)\)", line):
                template.c_compiler = match.group(1)
                print(f"Found C compiler: {template.c_compiler}")

            elif match := re.match(r"CPP_COMPILER\(([^)]+)\)", line):
                template.cpp_compiler = match.group(1)
                print(f"Found C++ compiler: {template.cpp_compiler}")

            elif match := re.match(r"CHECK_HEADER\(([^)]+)\)", line):
                template.headersrequired.append(match.group(1))
                print(f"Found required header: {match.group(1)}")

            elif match := re.match(r"CHECK_FUNCTION\((\S+)\s+(\S+)(?:\s+(.+))?\)", line):
                func = match.group(1)
                header = match.group(2)
                libs = match.group(3) if match.group(3) else ""
                template.functionsrequired.append((func, header, libs))
                print(f"Required function: {func} from {header}" +
                      (f" with {libs}" if libs else ""))

            elif match := re.match(r"CHECK_FUNCTION_OPT\((\S+)\s+(\S+)(?:\s+(.+))?\)", line):
                func = match.group(1)
                header = match.group(2)
                libs = match.group(3) if match.group(3) else ""
                template.functionsoptional.append((func, header, libs))
                print(f"Optional function: {func} from {header}" +
                      (f" with {libs}" if libs else ""))

            elif match := re.match(r"FILES\(([^)]+)\)", line):
                pattern = match.group(1).strip()
                template.file_patterns.append(pattern)
                print(f"Found file pattern: {pattern}")
            elif match := re.match(r"OUTPUT\(([^)]+)\)",line):
                template.outputname = match.group(1)

        print(template)
