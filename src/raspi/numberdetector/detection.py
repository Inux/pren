
import cv2
import numpy as np
import queue
#import pytesseract
from src.raspi.numberdetector.numberDetectionPython.camera import Window


class Detection():

    def __init__(self, cam):
        self.subscribers = set()
        self.cam = cam
        self.imageQueueStartSignal = self.cam.imageQueueStartSignal
        self.imageQueuePlateDetector = self.cam.imageQueueNumberDetector
        self.imageQueueNumberDetector = queue.Queue()
        self.win = Window()
        self.win.createTrackbar()

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

    def detectStartSignal(self, frame):
        origFrame = frame
        thresholdFrame = self.filterAndMorphOPStart(frame, 
                                                 self.win.getTrackbarValues(
                                                    self.win.threshTrackbar), 
                                                self.win.getTrackbarValues(
                                                     self.win.kernelTrackbar), 
                                                self.win.getTrackbarValues(
                                                    self.win.iteratorTrackbar))
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

    def detectPlate(self, frame):
        origFrame = frame
        thresholdFrame = self.filterAndMorphOPNumber2(frame, 
                                                self.win.getTrackbarValues(
                                                    self.win.threshTrackbar), 
                                                self.win.getTrackbarValues(
                                                    self.win.kernelTrackbar), 
                                                self.win.getTrackbarValues(
                                                    self.iteratorTrackbar))
        contours, hierarchy = cv2.findContours(
                                                thresholdFrame, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_NONE)
        try:
            for val in contours:
                if cv2.contourArea(val) > 500:
                    x, y, w, h = cv2.boundingRect(val)
                    if ((h > 30) and (h < 80) and (w > 20) and (w < 80)):
                        crop_image = thresholdFrame[y:y+(h+10), x:x+(w+10)]
                        return crop_image
                        cv2.rectangle(origFrame,
                                    (x, y),
                                    (x + w, y + h),
                                    (255, 0, 0), 2)
                        
        except:
            pass

    def startSignalWorker(self):
        runde = 0
        while True:
            try:
                frame = self.imageQueueStartSignal.get()
                result, threashold, origFrame = self.detectStartSignal(frame)
                cv2.imshow(self.win.windowWorkFrame, threashold)
                cv2.imshow(self.win.windowOriginalFrame, origFrame)
                if result > 0:
                    runde += 1
                    self.updateStartSignal(runde)
                if runde == 3:
                    break
                return runde
            except:
                pass

    def startPlateWorker(self):
        while True:
            try:
                frame = self.imageQueuePlateDetector.get()
                result = self.detectPlate(frame)
                self.imageQueueNumberDetector.put(result)
            except:
                pass
    
    def startTeseractWorker(self):
        while True:
            try:
                frame = self.ImageQueue.get()
                config = ('-l eng --oem 1 --psm 3')
                #print(pytesseract.image_to_string(frame, config=config))
            except:
                pass
    
    def register(self, who):
        self.subscribers.add(who)
    
    def unregister(self, who):
        self.subscribers.discard(who)
    
    def updateStartSignal(self, message):
        for subscriber in self.subscribers:
            subscriber.updateStartSignal(message)

    def updateNumberFound(self, number):
        for subscriber in self.subscribers:
            subscriber.notifyNumberFound(number)