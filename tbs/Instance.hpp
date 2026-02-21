#pragma once

#include <vector>
#include <string>
#include <tuple>

struct Instance
{
    std::vector<std::tuple<std::string,std::string,std::string>> Flags;
    std::vector<std::string> dirs;
};