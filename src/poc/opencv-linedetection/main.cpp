#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>

namespace {
    const cv::Scalar color = cv::Scalar(255, 255, 255);

    const int cannyTreshold = 300;
    const double cannTresholdRatio = 1.5;
    const int contourSizeTreshold = 550;

    cv::Mat prepareImage(cv::Mat src)
    {
        cv::Mat prepared;
        cvtColor(src, prepared, CV_BGR2GRAY);
        //cv::blur(prepared, prepared, cv::Size(5,5));
        return prepared;
    }

    cv::Mat applyCanny(cv::Mat src)
    {
        cv::Mat cdst;
        Canny(src, cdst, cannyTreshold, cannyTreshold*cannTresholdRatio, 3 );
        return cdst;
    }

    std::vector<std::vector<cv::Point> > getContours(cv::Mat src)
    {
        std::vector<std::vector<cv::Point> > contours;
        std::vector<cv::Vec4i> hierarchy;

        findContours(src, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, cv::Point(0, 0) );
        std::cout << "Found Contours: " << contours.size() << std::endl;

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
        std::cout << "Dropped Contours: " << dropped << std::endl;
        std::cout << "Useful Contours: " << useful << std::endl;

        return contoursFiltered;
    }

    cv::Mat getDrawing(cv::Mat src, std::vector<std::vector<cv::Point> > contours)
    {
        cv::Mat drawing = cv::Mat::zeros( src.size(), CV_8UC3 );
        std::vector<cv::Vec4i> hierarchy;

        for( int i = 0; i< contours.size(); i++ )
        {
            drawContours(drawing, contours, i, color, 2, cv::LineTypes::LINE_4, hierarchy, 0, cv::Point());
        }

        return drawing;
    }
}

int main(int argc, char** argv)
{
    const char* filename = argc >= 2 ? argv[1] : "";

    cv::Mat src = cv::imread(filename, 1);
    if(src.empty())
    {
        std::cout << "can not open " << filename << std::endl;
        return -1;
    }

    auto prepared = prepareImage(src);

    auto edges = applyCanny(prepared);

    auto contours = getContours(edges);
    contours = filterContours(contours, contourSizeTreshold);

    auto drawing = getDrawing(edges, contours);

    cv::imshow("Source", src);
    cv::imshow("Prepared", prepared);
    cv::imshow("Edges", edges);
    cv::imshow("Result", drawing);

    cv::waitKey(0);

    return 0;
}