#pragma once

#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>

#include "Template.hpp"
#include "Instance.hpp"

class TemplateParser
{
public:
    TemplateParser(Instance instance)
    {
        m_instance = instance;
    }
private:
    std::vector<std::string> ParseLineMaster(const std::string& line)
    {
        std::vector<std::string> cmdsargs;

        size_t open = line.find('(');
        size_t close = line.rfind(')');

        if (open == std::string::npos || close == std::string::npos || close < open)
            return std::vector<std::string>{};
        
        cmdsargs.push_back(line.substr(0,open));


        std::string inside = line.substr(open + 1, close - open - 1);
        std::stringstream ss(inside);

        std::string arg;

        while (ss >> arg)
            cmdsargs.push_back(arg);
        
        return cmdsargs;
    }
    void ParseMaster()
    {
        Template master;
        master.templatename = "Master";
        master.filename = "master.tbm";

        master.output = "Makefile";

        std::ifstream masterfile(master.filename);

        if (!masterfile)
        {
            
        }
    }
private:
    std::vector<Template> m_templates;
    Instance m_instance;

    std::string m_mastertitle;
};