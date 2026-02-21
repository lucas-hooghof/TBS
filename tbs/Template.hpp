#pragma once

#include <string>
#include <vector>
#include <tuple>

struct Template
{
    std::string C_Compiler;
    std::string CPP_Compiler;
    std::string Linker;
    std::string Assembler;

    std::vector<std::string> Defines;
    std::vector<std::string> LibraryDirs;
    std::vector<std::string> LibraryLinks;
    std::vector<std::string> IncludeDirs;

    std::vector<std::string> headersrequired;
    std::vector<std::tuple<std::string,std::string,std::string>> functionsrequired;
    std::vector<std::tuple<std::string,std::string,std::string>> functionsoptional;

    std::vector<std::string> LinkFlags;
    std::vector<std::string> CompileFlags;
    std::vector<std::string> AssembleFlags;
    std::string LinkerScript;

    std::vector<std::string> C_Files;
    std::vector<std::string> CPP_Files;
    std::vector<std::string> ASM_Files;

    std::vector<std::string> File_Patterns;

    std::string templatename;
    std::string filename;

    std::string output;
    std::vector<Template> Dependencies;

    std::vector<std::string> PreBuildCommands;
    std::vector<std::string> PostBuildCommands;
};