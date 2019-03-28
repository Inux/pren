#include <iostream>
#include <string>
#include <stdlib.h>
#include <opencv4/opencv2/opencv.hpp>
#include <opencv4/opencv2/video.hpp>
#include <opencv4/opencv2/imgproc.hpp>
#include <opencv4/opencv2/highgui.hpp>

using namespace cv;

class PlateDetec{

    public:
        PlateDetec(void);

        void setRPICameraSettings(void);

        void enableWindow(void);

        int showImage(void);

        Mat takePicture(void);

        Mat FindandDrawcontours(Mat pic, Mat original);



    private:
        const std::string frameWindow = "FrameWindow";

        VideoCapture cap;

        Mat applyFilters(Mat pic, double thresValue);

};
