
#include"PlateDetec.hpp"


PlateDetec::PlateDetec(void){
   cap = VideoCapture(-1);
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

void PlateDetec::enableWindow(std::string windowName, bool withTrackbar){
   namedWindow(windowName,1);
   if(withTrackbar) {
       createTrackbar("Thres", windowName, 0, 255, on_trckbar);
       createTrackbar("hmax", windowName, 0, 255, on_trckbar);
       createTrackbar("hmin", windowName, 0, 255, on_trckbar);
   }
}

Mat PlateDetec::applyFilters(Mat pic, double thresValue) {
    cvtColor(pic,pic,COLOR_BGR2GRAY);
    threshold(pic,pic,thresValue,255,THRESH_BINARY_INV);
    return pic;
}

void PlateDetec::FindandDrawcontours(Mat sourceFrame, Mat drawFrame, int hmax, int hmin){
    std::vector<std::vector<Point>> contours;
    std::vector<Vec4i> hierarchy;

    findContours(sourceFrame,contours,hierarchy,RETR_TREE,CHAIN_APPROX_SIMPLE,Point(0,0));
    for(int i = 0; i < hierarchy.size(); i++) {
        Rect rect = boundingRect(contours[i]);
        if((rect.height > hmin) && (rect.height < hmax)){
            rectangle(drawFrame,rect,(0,255,0),2,LINE_8,0);
        }
    }
}

int PlateDetec::showImage(void){
   if(!cap.isOpened()) return -1;
    enableWindow(WORKWINDOW,true);
    enableWindow(THRESWINDOW, false);
    Mat frame;
    Mat original;

   for(;;){
      cap >> frame;
      original = frame;

      double thres = (double) getTrackbarPos("Thres",WORKWINDOW);
      int hmax = getTrackbarPos("hmax",WORKWINDOW);
      int hmin = getTrackbarPos("hmin",WORKWINDOW);

      Mat filter = applyFilters(frame,thres);

      FindandDrawcontours(filter,original,hmax,hmin);
      imshow(THRESWINDOW,filter);
      imshow(WORKWINDOW,original);
      if(waitKey(30) >= 0) break;
   }
   return 0;
}


