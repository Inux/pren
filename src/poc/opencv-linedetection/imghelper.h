#pragma once

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <numeric>

namespace Img {
    constexpr int IMG_RESULT_SIZE = 400;
    constexpr int CANNY_THRESHOLD = 100;
    constexpr double CANNY_THRESHOLD_RATIO = 3;
    cv::Scalar CONTOUR_COLOR = cv::Scalar(255, 255, 255);
    cv::Scalar LINE_COLOR = cv::Scalar(255, 0, 0);

    /* resize an image */
    cv::Mat resizeImage(cv::Mat src, int resultSize=IMG_RESULT_SIZE)
    {
        int size = resultSize;
        bool isLandscape = false;
        float ratio = 0.f;
        if(src.cols > src.rows) {
            ratio = float(src.cols)/float(src.rows);
            isLandscape = true;
        } else {
            ratio = float(src.rows)/float(src.cols);
            isLandscape = false;
        }

        int newXsize = 0;
        int newYsize = 0;
        if(isLandscape) {
            newXsize = size * ratio;
            newYsize = size;
        } else {
            newXsize = size;
            newYsize = size * ratio;
        }

        cv::Mat dst;
        cv::resize(src, dst, cv::Size(newXsize, newYsize), 0, 0, cv::INTER_CUBIC);

        return dst;
    }

    cv::Mat applyGrayscale(cv::Mat src)
    {
        cv::Mat gdest;
        cvtColor(src, gdest, CV_BGR2GRAY);
        return gdest;
    }

    cv::Mat applyBlur(cv::Mat src)
    {
        cv::blur(src, src, cv::Size(3,3));
        return src;
    }

    cv::Mat applyCanny(cv::Mat src, int cannyThreshold=CANNY_THRESHOLD, double cannyThresholdRatio=CANNY_THRESHOLD_RATIO)
    {
        cv::Mat cdst;
        Canny(src, cdst, cannyThreshold, cannyThreshold*cannyThresholdRatio, 3 );
        return cdst;
    }

    cv::Mat applyContours(cv::Mat src, std::vector<std::vector<cv::Point> > contours, cv::Scalar color=CONTOUR_COLOR)
    {
        cv::Mat drawing = cv::Mat::zeros( src.size(), CV_8UC3 );
        std::vector<cv::Vec4i> hierarchy;

        for( int i = 0; i< contours.size(); i++ )
        {
            cv::drawContours(drawing, contours, i, color, 2, cv::LineTypes::LINE_4, hierarchy, 0, cv::Point());
        }

        return drawing;
    }

    cv::Mat applyLine(cv::Mat src, cv::Point from, cv::Point to, cv::Scalar color=LINE_COLOR)
    {
        cv::line(src, from, to, color, 2);
        return src;
    }
}