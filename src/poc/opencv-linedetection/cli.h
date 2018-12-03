#pragma once

#include <iostream>

#include "logger.h"
#include "argh.h"

namespace Cli {
    //Constants
    const std::string USAGE = "./main --filename=path/to/filename.png --contourMinSize=1000";

    struct CliParams {
        std::string filename;
        int contourMinSizeThreshold;
        int cannyThreshold;
        int cannyRatio;
        bool verbose;
        bool isValid;
    };

    CliParams parse(char** argv, CliParams defaultParams) {
        CliParams params;
        params.isValid = true;

        argh::parser cmdl(argv);

        if(cmdl({"--filename"}))
        {
            Log::info("CLI", "parse", "File: "+cmdl("filename").str());
            params.filename = cmdl("filename").str();
        }
        else
        {
            params.filename = "No Filename given";
            Log::err("CLI", "parse", "No Filename given. Usage: \n"+USAGE);
            params.isValid = false;
            return params; //abort, nothing todo without filename
        }

        std::string contourMinSize;
        if((cmdl({"--contourMinSize"}) >> contourMinSize))
        {
            Log::info("CLI", "parse", "Contour min. Size (pixel): '" + cmdl("contourMinSize").str() + "'");
            params.contourMinSizeThreshold = std::atoi(contourMinSize.c_str());
        }

        std::string cannyThreshold;
        if((cmdl({"--cannyThreshold"}) >> cannyThreshold))
        {
            Log::info("CLI", "parse", "Canny Threshold: '" + cmdl("cannyThreshold").str() + "'");
            params.cannyThreshold = std::atoi(cannyThreshold.c_str());
        }

        std::string cannyRatio;
        if((cmdl({"--cannyRatio"}) >> cannyRatio))
        {
            Log::info("CLI", "parse", "Canny Ratio: '" + cmdl("cannyRatio").str() + "'");
            params.cannyRatio = std::atoi(cannyRatio.c_str());
        }

        if (cmdl[{ "-v", "--verbose" }])
        {
            params.verbose = true;
            Log::setDebug(true);
            Log::info("Main", "parameterCheck" , "Verbose: 'true'");
        } else
        {
            params.verbose = false;
            Log::info("Main", "parameterCheck" , "Verbose: 'false'");
        }

        return params;
    }
}