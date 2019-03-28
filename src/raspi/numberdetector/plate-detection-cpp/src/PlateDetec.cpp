
#include"PlateDetec.hpp"


PlateDetec::PlateDetec(void){
   cap = VideoCapture(0);
}

void on_trckbar(int, void*){
}

void PlateDetec::setRPICameraSettings(void){
   cap.set(CAP_PROP_FRAME_WIDTH, 640);
   cap.set(CAP_PROP_FRAME_HEIGHT, 480);
   cap.set(CAP_PROP_BRIGHTNESS,0.5);
   cap.set(CAP_PROP_CONTRAST, 0.5);
   cap.set(CAP_PROP_SATURATION,0.5);
}

void PlateDetec::enableWindow(void){
   namedWindow(frameWindow,1);
   createTrackbar("Thres",frameWindow,0,255,on_trckbar);
   createTrackbar("hmax",frameWindow,0,255,on_trckbar);
   createTrackbar("hmin",frameWindow,0,255,on_trckbar);
}

Mat PlateDetec::applyFilters(Mat pic, double thresValue) {
    cvtColor(pic,pic,COLOR_BGR2GRAY);
    threshold(pic,pic,thresValue,255,THRESH_BINARY_INV);
    return pic;
}

Mat PlateDetec::FindandDrawcontours(Mat pic, Mat original){
    std::vector<std::vector<Point>> contours;
    std::vector<Vec4i> hierarchy;

    findContours(pic,contours,hierarchy,RETR_TREE,CHAIN_APPROX_SIMPLE,Point(0,0));
    int hmax = getTrackbarPos("hmax",frameWindow);
    int hmin = getTrackbarPos("hmin",frameWindow);
    for(int i = 0; i < hierarchy.size(); i++) {
        Rect rect = boundingRect(contours[i]);
        if((rect.height > hmin) && (rect.height < hmax)){
            rectangle(original,rect,(0,255,0),2,LINE_8,0);
        }
    }


}

int PlateDetec::showImage(void){
   if(!cap.isOpened()) return -1;

   for(;;){
      Mat frame;
      Mat original;
      cap >> frame;
      original = frame;
      double i = (double) getTrackbarPos("Thres",frameWindow);
      Mat filter = applyFilters(frame,i);
      FindandDrawcontours(filter,original);
      imshow(frameWindow,original);
      if(waitKey(30) >= 0) break;
   }
   return 0;
}


