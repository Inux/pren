#pragma once

#include <iostream>

namespace {
    bool DEBUG_MODE = false;

    void write(const std::string& level, const std::string& component, const std::string& action, const std::string& message)
    {
        std::cout << level << ": " << component << "." << action << " -> " << message << std::endl;
    }
}

namespace Log {
    void setDebug(bool debug) {
        DEBUG_MODE = debug;
    }

    bool isDebug() {
        return DEBUG_MODE;
    }

    void info(const std::string& component, const std::string& action, const std::string& message)
    {
        write("INFO", component, action, message);
    }

    void err(const std::string& component, const std::string& action, const std::string& message)
    {
        write("ERROR", component, action, message);
    }

    void dbg(const std::string& component, const std::string& action, const std::string& message)
    {
        if (DEBUG_MODE) write("DEBUG", component, action, message);
    }
}