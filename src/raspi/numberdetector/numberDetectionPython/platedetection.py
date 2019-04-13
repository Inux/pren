
import cv2
import numpy as np
#from numberReco import NumberReco
#import pydevd_pycharm
#pydevd_pycharm.settrace('192.168.0.31', port=3265, stdoutToServer=True, stderrToServer=True)



def nothing(x):
    pass


class PlateDetection:




    def __init__(self):
        #self.nRec = NumberReco()
        self.cap = cv2.VideoCapture(-1)
        self.windowName = "workwindow"
        self.thresTrackbar = "ThresTrackbar"
        self.hmaxTrackbar = "HmaxTrackbar"
        self.hminTrackbar = "HminTrackbar"
        self.windowOrigin = "OriginWIndow"

        self.thresFix = 1
        self.hmaxFix = 77
        self.hminFix = 58

    def initCam(self):
        w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        b = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        c = self.cap.get(cv2.CAP_PROP_CONTRAST)
        S = self.cap.get(cv2.CAP_PROP_SATURATION)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        #self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
        #self.cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
        #self.cap.set(cv2.CAP_PROP_SATURATION, 0.5)

        print("Sat: " + str(S))
        print("Contr:" + str(c))
        print("Brigh: " + str(b))

    def createTrackbar(self,imgWindow):
        cv2.createTrackbar(self.thresTrackbar, imgWindow, 0, 255, nothing)
        cv2.createTrackbar(self.hmaxTrackbar, imgWindow, 0, 150, nothing)
        cv2.createTrackbar(self.hminTrackbar, imgWindow, 0, 150, nothing)
        thres = cv2.getTrackbarPos(self.thresTrackbar, self.windowName)
        hmin = cv2.getTrackbarPos(self.hminTrackbar, self.windowName)
        hmax = cv2.getTrackbarPos(self.hmaxTrackbar, self.windowName)

    def showWebcam(self):


        cv2.namedWindow(self.windowName)
        cv2.namedWindow(self.windowOrigin)

        self.createTrackbar(self.windowName)

        thres = cv2.getTrackbarPos(self.thresTrackbar, self.windowName)
        hmin = cv2.getTrackbarPos(self.hminTrackbar, self.windowName)
        hmax = cv2.getTrackbarPos(self.hmaxTrackbar, self.windowName)

        cv2.createTrackbar('iterator', self.windowName, 1, 10, nothing)
        cv2.createTrackbar('kernel', self.windowName, 1, 30, nothing)

        iterator = cv2.getTrackbarPos('iterator', self.windowName)
        kernelI = cv2.getTrackbarPos('kernel', self.windowName)


        while(True):


            ret, frame = self.cap.read()
            orignFram = frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, thresh1 = cv2.threshold(gray,thres,255,cv2.THRESH_TOZERO)

            kernel1 = np.ones((kernelI, kernelI), np.uint8)



            thresh1 = cv2.dilate(thresh1, kernel1, iterations=iterator)

            iterator = cv2.getTrackbarPos('iterator', self.windowName)
            kernelI = cv2.getTrackbarPos('kernel', self.windowName)


            contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



            try:

                for val in contours:
                    x, y, w, h = cv2.boundingRect(val)
                    if ((h > hmin) and (h < hmax)):
                        cv2.rectangle(orignFram, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        rect = [x,y,w,h]
                        #self.nRec.recoNumber(thresh1,rect)
            except:
                pass


            cv2.imshow(self.windowOrigin,orignFram)
            cv2.imshow(self.windowName,thresh1)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            thres = cv2.getTrackbarPos(self.thresTrackbar, self.windowName)
            hmin = cv2.getTrackbarPos(self.hminTrackbar, self.windowName)
            hmax = cv2.getTrackbarPos(self.hmaxTrackbar, self.windowName)



        self.cap.release()




def main():
    plateDetection = PlateDetection()
    plateDetection.showWebcam()

if __name__=='__main__':
    main()