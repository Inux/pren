
import cv2
import numpy as np
import time
import pytesseract
import queue


def nothing(x):
    pass


class PlateDetection:

    def __init__(self):
        # self.numberReco = NumberReco.NumberReco()
        self.windowTrackbar = "trackbarWindow"
        self.windowWorkFrame = "workFrameWindow"
        self.windowOriginalFrame = "OriginalFrameWindow"

        self.threshTrackbar = "Threshold"
        self.hMaxTrackbar = "HMax"
        self.hMinTrackbar = "HMin"
        self.iteratorTrackbar = "iterator"
        self.kernelTrackbar = "Kernel"
        self.imageQueueStartSignal = queue.Queue()
        self.imageQueueNumberDetector = queue.Queue()
        self.evt = Event()
        
    def initCam(self, cap):
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 70)
        cap.set(cv2.CAP_PROP_CONTRAST, 30)
        cap.set(cv2.CAP_PROP_SATURATION, 30)
        cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 45)

    def createTrackbar(self):
        cv2.namedWindow(self.windowTrackbar)
        cv2.createTrackbar(self.threshTrackbar, self.windowTrackbar, 0, 255, nothing)
        cv2.createTrackbar(self.hMaxTrackbar, self.windowTrackbar, 0, 150, nothing)
        cv2.createTrackbar(self.hMinTrackbar, self.windowTrackbar, 0, 150, nothing)
        cv2.createTrackbar(self.iteratorTrackbar, self.windowTrackbar, 0, 255, nothing)
        cv2.createTrackbar(self.kernelTrackbar, self.windowTrackbar, 1, 30, nothing)

    def getTrackbarValues(self, trackbar):
        return{
            self.threshTrackbar: cv2.getTrackbarPos(self.threshTrackbar, self.windowTrackbar),
            self.hMaxTrackbar: cv2.getTrackbarPos(self.hMaxTrackbar, self.windowTrackbar),
            self.hMinTrackbar: cv2.getTrackbarPos(self.hMinTrackbar, self.windowTrackbar),
            self.iteratorTrackbar: cv2.getTrackbarPos(self.iteratorTrackbar, self.windowTrackbar),
            self.kernelTrackbar: cv2.getTrackbarPos(self.kernelTrackbar, self.windowTrackbar)
        }.get(trackbar, 0)

    def filterAndMorphOPNumber2(self, frame, threashold, kernel, iterator):
        x, y, w, h = 50, 50, 400, 500
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh1 = cv2.threshold(blur, threashold, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresh1 = thresh1[y:y + h, x:x + w]
        return thresh1

    def filterAndMorphOPNumber(self, frame, threshold, kernel, iterator):
        kernel1 = np.ones((kernel, kernel), np.uint8)
        farb = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([0, 0, 222])
        upper_blue = np.array([255, 8, 255])

        mask = cv2.inRange(farb, lower_blue, upper_blue)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        

        return thresh1

    def filterAndMorphOPStart(self, frame, threshold, kernel, iterator):
        kernel1 = np.ones((15, 25), np.uint8)
        farb = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([85, 151, 30])
        upper_blue = np.array([255, 255, 255])
        mask = cv2.inRange(farb, lower_blue, upper_blue)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        color = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
        gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

        opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel1)

        return opening

    def changeFrame(self):
        img = cv2.imread('Z:/number9.jpg')
        self.createTrackbar()

        while(True):
            orignFram = cv2.imread('Z:/number9.jpg')
            thresholdFrame = self.filterAndMorphOPNumber2(img, self.getTrackbarValues(self.threshTrackbar), self.getTrackbarValues(self.kernelTrackbar), self.getTrackbarValues(self.iteratorTrackbar))
            try:
                contours, hierarchy = cv2.findContours(
                                        thresholdFrame, 
                                        cv2.RETR_TREE, 
                                        cv2.CHAIN_APPROX_NONE)
            
                for val in contours:
                    x, y, w, h = cv2.boundingRect(val)
                    if ((h > 35) and (h < 70) and (w > self.getTrackbarValues(self.hMinTrackbar)) and (w < self.getTrackbarValues(self.hMaxTrackbar))):
                        # self.ImageQueue.put(img)
                        cv2.rectangle(orignFram,
                                    (x, y),
                                    (x + w, y + h),
                                    (255, 0, 0), 2)

            except:
                pass


            cv2.imshow(self.windowWorkFrame, thresholdFrame)
            cv2.imshow(self.windowOriginalFrame, orignFram)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def detectStartSignal(self, frame):
        origFrame = frame
        thresholdFrame = self.filterAndMorphOPStart(frame, 
                                                    self.getTrackbarValues(
                                                        self.threshTrackbar), 
                                                    self.getTrackbarValues(
                                                        self.kernelTrackbar), 
                                                    self.getTrackbarValues(
                                                        self.iteratorTrackbar))
        contours, hierarchy = cv2.findContours(
                                                thresholdFrame, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_NONE)
        result = 0
        try:
            for val in contours:
                x, y, w, h = cv2.boundingRect(val)
                if ((h > 15) and (h < 25) and ((w > 50) and (w < 80))):
                    cv2.rectangle(origFrame,
                                  (x, y),
                                  (x + w, y + h),
                                  (255, 0, 0), 2)
                    result = result + 1
        except:
            pass
        
        if(result == 2):
            return (1, thresholdFrame, origFrame)
        else:
            return (0, thresholdFrame, origFrame)

    def routineDetectNumber(self, cap):
        self.createTrackbar()
        index = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            orig = frame
            thresholdFrame = self.filterAndMorphOPNumber2(frame, self.getTrackbarValues(self.threshTrackbar), self.getTrackbarValues(self.kernelTrackbar), self.getTrackbarValues(self.iteratorTrackbar))
            try:
                contours, hierarchy = cv2.findContours(
                                        thresholdFrame, 
                                        cv2.RETR_TREE, 
                                        cv2.CHAIN_APPROX_NONE)
            
                for val in contours:
                    if cv2.contourArea(val) > 500:
                        x, y, w, h = cv2.boundingRect(val)
                        if ((h > 30) and (h < 80) and (w > 20) and (w < 80)):
                            # crop_image = thresholdFrame[y:y+(h+10), x:x+(w+10)]
                            # self.ImageQueue.put(crop_image)
                            cv2.rectangle(orig,
                                        (x, y),
                                        (x + w, y + h),
                                        (255, 0, 0), 2)

            except:
                pass

            cv2.imshow(self.windowWorkFrame, thresholdFrame)
            cv2.imshow(self.windowOriginalFrame, orig)
            time.sleep(0.05)
            index = index+1


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def routineDetectStartSignal(self, cap, window, manipulation, save):
        startSignalFound = False

        if(save):
            forcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi', forcc, 20.0, (640, 480))

        while(True):
            ret, frame = cap.read()
            startSignalFound, thresholdFrame, origFrame = self.detectStartSignal(frame)

            if(window):
                cv2.imshow(self.windowOriginalFrame, origFrame)
                cv2.imshow(self.windowWorkFrame, thresholdFrame)

            if(save):
                out.write(frame)

            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

            time.sleep(0.05)

    def cameraWorker(self, cap):
        while True:
            ret, frame = cap.read()
            self.imageQueueStartSignal.put(frame)
            self.imageQueueNumberDetector(frame)

    def startSignalWorker(self):
        runde = 0
        while True:
            try:
                frame = self.imageQueueStartSignal.get()
                result, _, _ = self.detectStartSignal(frame)
                if result > 0:
                    runde += 1
                return runde
            except:
                pass

    def tesseractWorker(self):
        while True:
            try:
                frame = self.ImageQueue.get()
                config = ('-l eng --oem 1 --psm 3')
                print(pytesseract.image_to_string(frame, config= config))
            except:
                pass

    def kerasWorker(self):
        while True:
            try:
                frame = self.ImageQueue.get()
                self.numberReco.recoNumber(frame)
            except:
                pass


def main():
    cap = cv2.VideoCapture(-1)
    plateDetection = PlateDetection()
    time.sleep(2)
    # t = threading.Thread(target= plateDetection.kerasWorker)
    # t2 = threading.Thread(target= plateDetection.kerasWorker)
    # t.start()
    # t2.start()
    # plateDetection.routineDetectStartSignal(cap, True, False, False)
    plateDetection.routineDetectStartSignal(cap, True, False, False)
    # plateDetection.changeFrame()


if __name__ == '__main__':
    main()
