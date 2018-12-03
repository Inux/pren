#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <numeric>

#include "logger.h"
#include "cli.h"
#include "imghelper.h"

namespace {
    const Cli::CliParams defaultParams = {.filename = "", .contourMinSizeThreshold = 100, .cannyThreshold = 200, .cannyRatio=3, .verbose = false, .isValid = false};

    void printImageStats(cv::Mat img)
    {
        Log::dbg("Main", "printImageStats", "X: " + std::to_string(img.cols) + ", Y: " + std::to_string(img.rows));
    }

    cv::Mat prepareImage(cv::Mat src)
    {
        src = Img::resizeImage(src);
        src = Img::applyGrayscale(src);
        src = src > 128;
        src = Img::applyBlur(src);
        return src;
    }

    std::vector<std::vector<cv::Point> > getContours(cv::Mat src)
    {
        std::vector<std::vector<cv::Point> > contours;
        std::vector<cv::Vec4i> hierarchy;

        cv::findContours(src, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_TC89_KCOS, cv::Point(0, 0));
        Log::dbg("Main", "getContours", "Contours Count: " + std::to_string(contours.size()));

        return contours;
    }

    std::vector<std::vector<cv::Point> > filterContours(std::vector<std::vector<cv::Point> > contours, int sizeThreshold)
    {
        int useful = 0;
        int dropped = 0;
        std::vector<std::vector<cv::Point> > contoursFiltered;
        for( int i = 0; i< contours.size(); i++ )
        {
            if(contours[i].size() >= sizeThreshold)
            {
                contoursFiltered.push_back(contours[i]);
                useful++;
            } else {
                dropped++;
            }
        }
        Log::dbg("Main", "filterContours", "Dropped Contours: " + std::to_string(dropped));
        Log::dbg("Main", "filterContours", "Useful Contours: " + std::to_string(useful));

        return contoursFiltered;
    }

    void printContoursStats(std::vector<std::vector<cv::Point> > contours)
    {
        for(int i = 0; i < contours.size(); i++)
        {
            auto contour = contours[i];
            Log::dbg("Main", "printContourStats", "Contour " + std::to_string(i) + " Points: " + std::to_string(contour.size()));

            std::vector<float> vslope;
            for(int i = 0; i < contour.size()-1; i++)
            {
                auto dx = contour[i+1].x - contour[i].x;
                auto dy = contour[i+1].y - contour[i].y;
                if(dy != 0)
                {
                     vslope.push_back(float(dx)/float(dy));
                }
            }
            float avgSlope = std::accumulate(vslope.begin(), vslope.end(), 0.0)/vslope.size();

            Log::dbg("Main", "printContourStats", "Average slope = " + std::to_string(avgSlope));
        }
    }
}

int main(int argc, char** argv)
{
    Cli::CliParams params = Cli::parse(argv, defaultParams);
    if(not params.isValid) {
        Log::err("Main", "parameterCheck" , "invalid CLI params");
        return 1;
    }

    cv::Mat src = cv::imread(params.filename, 1);
    if(src.empty())
    {
        Log::err("Main", "parameterCheck" , "can't open file path: '" + params.filename + "'");
        return 1;
    }

    if(Log::isDebug())
        printImageStats(src);

    auto prepared = prepareImage(src);

    auto edges = Img::applyCanny(prepared, params.cannyThreshold, params.cannyRatio);

    auto contours = getContours(edges);
    contours = filterContours(contours, params.contourMinSizeThreshold);

    printContoursStats(contours);

    auto drawing = Img::applyContours(edges, contours);
    Img::applyLine(drawing, cv::Point(drawing.cols/2, 0), cv::Point(drawing.cols/2, drawing.rows));

    if(Log::isDebug())
    {
        cv::imshow("Prepared", prepared);
        cv::imshow("Edges", edges);
    }

    cv::imshow("Result", drawing);

    cv::waitKey(0);

    return 0;
}