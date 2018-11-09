#include <iostream>

#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <tesseract/publictypes.h>
#include <tesseract/baseapi.h>

/* Helper Functions */
std::string clean_string(std::string s) {
    size_t i = 0;

    while (i < s.length()) {
        i = s.find_first_of(" \t\r\n", i);
        s.erase(i);
    }
    return s;
}

cv::Mat prepare_img(cv::Mat img) {
    cv::resize(img, img, cv::Size2f(), 1.5f, 1.5f, cv::INTER_CUBIC);
    cv::cvtColor(img, img, cv::COLOR_BGR2GRAY);
    cv::dilate(img, img, cv::Mat(), cv::Point(1, 1), 2, 1, 1);
    cv::erode(img, img, cv::Mat(), cv::Point(1, 1), 2, 1, 1);
    cv::GaussianBlur(img, img, cv::Size( 5, 5), 0, 0);
    cv::threshold(img, img, 0, 255, cv::THRESH_BINARY|cv::THRESH_OTSU);

    cv::imwrite("result_prepare_img.jpg", img);

    return img;
}

bool is_number(const std::string& s)
{
    auto cs = clean_string(s);
    std::string::const_iterator it = cs.begin();
    while (it != cs.end() && std::isdigit(*it)) ++it;
    return !cs.empty() && it == cs.end();
}

/* End Helper Functions */

/* Create Contour Image - Creates a image with rectangles arround detected Objects */
void createContourImage(cv::Mat src)
{
    cv::Mat gray;
    cv::cvtColor(src, gray, CV_BGR2GRAY);
    cv::threshold(gray, gray, 200, 255, cv::THRESH_BINARY_INV);

    std::vector<std::vector<cv::Point> > contours;
    std::vector<cv::Vec4i> hierarchy;

    cv::findContours(gray, contours, hierarchy,CV_RETR_CCOMP, CV_CHAIN_APPROX_SIMPLE);

    for( int i = 0; i< contours.size(); i=hierarchy[i][0] )
    {
        cv::Rect r= cv::boundingRect(contours[i]);
        cv::rectangle(src, cv::Point(r.x,r.y), cv::Point(r.x+r.width,r.y+r.height), cv::Scalar(0,0,255), 1, 8, 0);
    }

    cv::imwrite("result_contours.jpg", src);
}

/* Predict Number - Predicts if a number is in the Image */
std::string predictNumber(cv::Mat img) {
    tesseract::TessBaseAPI* ocr = new tesseract::TessBaseAPI();
    ocr->SetVariable("tessedit_char_blacklist", "!?@#$%&*()<>_-+=/:;'\"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz");
    ocr->SetVariable("tessedit_char_whitelist", "0123456789");
    ocr->SetVariable("classify_bln_numeric_mode", "1");

    // Initialize tesseract to use English (eng)
    ocr->Init(NULL, "eng", tesseract::OEM_DEFAULT);
    ocr->SetPageSegMode(tesseract::PSM_SINGLE_CHAR);
    ocr->SetImage(img.data, img.cols, img.rows, 3, img.step);

    // Run Tesseract OCR on image
    std::string outText = std::string(ocr->GetUTF8Text());

    delete ocr;
    ocr = nullptr;

    return outText;
}

int main( int argc, char** argv )
{
    if(argc <= 1) {
        //Abort if no image is available
        std::cout << "No Image. Abort..." << std::endl;
        return EXIT_FAILURE;
    }
    std::string imgPath = argv[1];
    std::cout << "Using Image: " << imgPath << std::endl;

    cv::Mat img = cv::imread(imgPath, 1), gray, temp;
    prepare_img(img);

    cv::cvtColor(img, gray, CV_BGR2GRAY);
    gray = gray > 127;

    std::vector<std::vector<cv::Point> > contours;
    std::vector<cv::Vec4i> hierarchy;

    findContours(gray, contours, hierarchy,
                 CV_RETR_CCOMP, cv::CHAIN_APPROX_SIMPLE);

    cv::Rect minRect;

    std::string detectedText = predictNumber(img);
    if(is_number(detectedText)) {
        std::cout << "Detected Number: '" << std::stoi(detectedText) << "'" << std::endl;
    } else {
        std::cout << "No Number Detected! Detected Value: '" << detectedText << "'" << std::endl;
    }

    createContourImage(img);
}