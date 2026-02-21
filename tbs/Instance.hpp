#pragma once

#include <vector>
#include <string>
#include <tuple>

class Instance
{
public:
    Instance() = default;
    ~Instance() = default;

    std::vector<std::tuple<std::string,std::string,std::string>> Flags;
    std::vector<std::string> dirs;
};