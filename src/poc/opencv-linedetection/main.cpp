#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#include <iostream>

void help()
{
    std::cout << "\nThis program demonstrates line finding with the Hough transform.\n"
            "Usage:\n"
            "./houghlines <image_name>, Default is pic1.jpg\n" << std::endl;
}

int main(int argc, char** argv)
{
    const char* filename = argc >= 2 ? argv[1] : "pic1.jpg";

    cv::Mat src = cv::imread(filename, 0);
    if(src.empty())
    {
        help();
        std::cout << "can not open " << filename << std::endl;
        return -1;
    }

    cv::Mat dst, cdst;
    cv::Canny(src, dst, 50, 200, 3);
    cv::cvtColor(dst, cdst, CV_GRAY2BGR);

    std::vector<cv::Vec4i> lines;
    cv::HoughLinesP(dst, lines, 1, CV_PI/180, 50, 50, 10 );
    for( size_t i = 0; i < lines.size(); i++ )
    {
        cv::Vec4i l = lines[i];
        line( cdst, cv::Point(l[0], l[1]), cv::Point(l[2], l[3]), cv::Scalar(0,0,255), 3, CV_AA);
    }

    cv::imshow("source", src);
    cv::imshow("detected lines", cdst);

    cv::waitKey();

    return 0;
}