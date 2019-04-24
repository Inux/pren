
import cv2
import numpy as np
from queue import Queue
from threading import Thread
# import pydevd_pycharm
# pydevd_pycharm.settrace('192.168.0.31', port=3265, stdoutToServer=True, stderrToServer=True)


def nothing(x):
    pass


class PlateDetection:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.camQueue = Queue(maxsize=10)
        print(str(self.camQueue.empty))

        self.windowTrackbar = "trackbarWindow"
        self.windowWorkFrame = "workFrameWindow"
        self.windowOriginalFrame = "OriginalFrameWindow"

        self.threshTrackbar = "Threshold"
        self.hMaxTrackbar = "HMax"
        self.hMinTrackbar = "HMin"
        self.iteratorTrackbar = "iterator"
        self.kernelTrackbar = "Kernel"

    def initCam(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
        self.cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
        self.cap.set(cv2.CAP_PROP_SATURATION, 0.5)

    def createTrackbar(self):
        cv2.namedWindow(self.windowTrackbar)
        cv2.createTrackbar(self.threshTrackbar, self.windowTrackbar, 0, 255, nothing)
        cv2.createTrackbar(self.hMaxTrackbar, self.windowTrackbar, 0, 150, nothing)
        cv2.createTrackbar(self.hMinTrackbar, self.windowTrackbar, 0, 150, nothing)
        cv2.createTrackbar(self.iteratorTrackbar, self.windowTrackbar, 0, 10, nothing)
        cv2.createTrackbar(self.kernelTrackbar, self.windowTrackbar, 0, 30, nothing)

    def getTrackbarValues(self, trackbar):
        return{
            self.threshTrackbar: cv2.getTrackbarPos(self.threshTrackbar,self.windowTrackbar),
            self.hMaxTrackbar: cv2.getTrackbarPos(self.threshTrackbar,self.windowTrackbar),
            self.hMinTrackbar: cv2.getTrackbarPos(self.threshTrackbar,self.windowTrackbar),
            self.iteratorTrackbar: cv2.getTrackbarPos(self.threshTrackbar,self.windowTrackbar),
            self.kernelTrackbar: cv2.getTrackbarPos(self.threshTrackbar,self.windowTrackbar)
        }.get(trackbar,0)

    def filterAndMorphOP(self, frame, threshold, kernel, iterator):
        kernel1 = np.ones((kernel, kernel), np.uint8)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, threshold, 255, cv2.THRESH_TOZERO)
        thresh1 = cv2.dilate(thresh1, kernel1, iterations=iterator)
        return thresh1

    def camWorker(self):
        while True:
            ret, frame = self.cap.read()
            self.camQueue.put(frame)

    def filterWorker(self):
        while True:
            try:
                frame = self.camQueue.get()
                self.filterAndMorphOP(frame, self.getTrackbarValues(self.threshTrackbar), self.getTrackbarValues(self.kernelTrackbar), self.getTrackbarValues(self.iteratorTrackbar))
            except:
                pass

    def showWebcam(self):

        cv2.namedWindow(self.windowOriginalFrame)
        self.createTrackbar()

        while(True):
            ret, frame = self.cap.read()
            orignFram = frame
            thresholdFrame = self.filterAndMorphOP(frame,self.getTrackbarValues(self.threshTrackbar),self.getTrackbarValues(self.kernelTrackbar),self.getTrackbarValues(self.iteratorTrackbar))

            contours, hierarchy = cv2.findContours(thresholdFrame,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            try:
                for val in contours:
                    x, y, w, h = cv2.boundingRect(val)
                    if ((h > self.getTrackbarValues(self.hMinTrackbar)) and (h < self.getTrackbarValues(self.hMaxTrackbar))):
                        cv2.rectangle(orignFram, (x, y), (x + w, y + h), (0, 255, 0), 2)
            except:
                pass

            cv2.imshow(self.windowTrackbar,thresholdFrame)
            cv2.imshow(self.windowOriginalFrame,orignFram)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()


def main():
    plateDetection = PlateDetection()
    plateDetection.initCam()
    plateDetection.createTrackbar()

    camThread = Thread(target=plateDetection.camWorker)
    filterThread = Thread(target=plateDetection.filterWorker)
    camThread.start()
    filterThread.start()
    camThread.join()
    filterThread.join()


if __name__=='__main__':
    main()