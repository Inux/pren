#include <iostream>
#include <string>
#include <stdlib.h>
#include <ctime>
#include <opencv4/opencv2/opencv.hpp>
#include <opencv4/opencv2/video.hpp>
#include <opencv4/opencv2/imgproc.hpp>
#include <opencv4/opencv2/highgui.hpp>

using namespace cv;

class PlateDetec{

    public:
        PlateDetec(void);

        void setRPICameraSettings(void);

        void enableWindow(std::string windowName, bool withTrackbar);

        int showImage(void);

        Mat takePicture(void);

        void FindandDrawcontours(Mat sourceFrame, Mat drawFrame, int hmax, int hmin);



    private:

        const std::string THRESWINDOW       = "ThresWindow";
        const std::string WORKWINDOW        = "Workwindow";

        VideoCapture cap;

        Mat applyFilters(Mat pic, double thresValue);

};
