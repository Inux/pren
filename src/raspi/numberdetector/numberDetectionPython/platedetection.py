
import cv2
import numpy as np

# import pydevd_pycharm
# pydevd_pycharm.settrace('192.168.0.31', port=3265, stdoutToServer=True, stderrToServer=True)


def nothing(x):
    pass


class PlateDetection:

    def __init__(self):
        self.cap = cv2.VideoCapture(-1)

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
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 70)
        self.cap.set(cv2.CAP_PROP_CONTRAST, 30)
        self.cap.set(cv2.CAP_PROP_SATURATION, 30)
        self.cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 45)

    def createTrackbar(self):
        cv2.namedWindow(self.windowTrackbar)
        cv2.createTrackbar(self.threshTrackbar, self.windowTrackbar, 0, 255, nothing)
        cv2.createTrackbar(self.hMaxTrackbar, self.windowTrackbar, 0, 150, nothing)
        cv2.createTrackbar(self.hMinTrackbar, self.windowTrackbar, 0, 150, nothing)
        cv2.createTrackbar(self.iteratorTrackbar, self.windowTrackbar, 0, 255, nothing)
        cv2.createTrackbar(self.kernelTrackbar, self.windowTrackbar, 0, 255, nothing)

    def getTrackbarValues(self, trackbar):
        return{
            self.threshTrackbar: cv2.getTrackbarPos(self.threshTrackbar, self.windowTrackbar),
            self.hMaxTrackbar: cv2.getTrackbarPos(self.hMaxTrackbar, self.windowTrackbar),
            self.hMinTrackbar: cv2.getTrackbarPos(self.hMinTrackbar, self.windowTrackbar),
            self.iteratorTrackbar: cv2.getTrackbarPos(self.iteratorTrackbar, self.windowTrackbar),
            self.kernelTrackbar: cv2.getTrackbarPos(self.kernelTrackbar, self.windowTrackbar)
        }.get(trackbar, 0)

    def filterAndMorphOPNumber(self, frame, threshold, kernel, iterator):
        #kernel1 = np.ones((kernel, kernel), np.uint8) #4
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 190, 255, cv2.THRESH_TOZERO) #179
        #thresh1 = cv2.dilate(thresh1, kernel1, iterations=1)
        #ret, thresh1 = cv2.threshold(thresh1, iterator, 255, cv2.THRESH_BINARY)
        return thresh1

    def filterAndMorphOPStart(self, frame, threshold, kernel, iterator):
        kernel1 = np.ones((kernel, kernel), np.uint8) 
        frame2 = frame
        farb = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([threshold, iterator, 188])
        upper_blue = np.array([180, 255, 255])
        mask = cv2.inRange(farb, lower_blue, upper_blue)
        res = cv2.bitwise_and(frame2, frame2, mask=mask)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)


        #ret, thresh1 = cv2.threshold(gray, threshold, 255, cv2.THRESH_TOZERO) #179
        ret, thresh1 = cv2.threshold(gray, kernel, 255, cv2.THRESH_BINARY)
        #thresh1 = cv2.erode(res, kernel1, iterations=1)
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

    def showCamNumber(self):
        cv2.namedWindow(self.windowOriginalFrame)
        self.createTrackbar()

        while(True):
            ret, frame = self.cap.read()
            frame = cv2.flip(frame,-1)
            orignFram = frame
            thresholdFrame = self.filterAndMorphOPNumber(frame, self.getTrackbarValues(self.threshTrackbar), self.getTrackbarValues(self.kernelTrackbar), self.getTrackbarValues(self.iteratorTrackbar))


            contours, hierarchy = cv2.findContours(thresholdFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            try:
                for val in contours:
                    x, y, w, h = cv2.boundingRect(val)
                    if ((h > 54 and (h < 74)) and (w > 24 and w < 50)):
                        cv2.rectangle(orignFram, (x, y), (x + w, y + h), (0, 255, 0), 2)
            except:
                pass

            cv2.imshow(self.windowTrackbar, thresholdFrame)
            cv2.imshow(self.windowOriginalFrame, orignFram)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()

    def showCamStart(self):
        cv2.namedWindow(self.windowOriginalFrame)
        self.createTrackbar()

        while(True):
            ret, frame = self.cap.read()
            frame = cv2.flip(frame,-1)
            orignFram = frame
            thresholdFrame = self.filterAndMorphOPStart(frame, self.getTrackbarValues(self.threshTrackbar), self.getTrackbarValues(self.kernelTrackbar), self.getTrackbarValues(self.iteratorTrackbar))


            #contours, hierarchy = cv2.findContours(thresholdFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #try:
            #    for val in contours:
            #        x, y, w, h = cv2.boundingRect(val)
            #        if ((h > self.getTrackbarValues(self.hMinTrackbar)) and (h < self.getTrackbarValues(self.hMaxTrackbar))): #hmax 105 hmin74
            #            cv2.rectangle(orignFram, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #except:
            #    pass

            cv2.imshow(self.windowTrackbar, thresholdFrame)
            cv2.imshow(self.windowOriginalFrame, orignFram)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()

    def saveMovieFile(self):
        forcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi',forcc,20.0,(640,480))
        cv2.namedWindow(self.windowOriginalFrame)
        self.createTrackbar()
        while(True):
            ret, frame = self.cap.read()
            frame = cv2.flip(frame,-1)
            out.write(frame)
            cv2.imshow(self.windowTrackbar, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                break


def main():
    plateDetection = PlateDetection()
    plateDetection.initCam()
    plateDetection.createTrackbar()
    plateDetection.saveMovieFile()

    
if __name__ == '__main__':
    main()
