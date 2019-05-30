
import queue
import cv2


class Camera():

    def __init__(self):
        self.cap = cv2.VideoCapture(-1)
        self.imageQueueStartSignal = queue.Queue()
        self.imageQueueNumberDetector = queue.Queue()

    def initCam(self, cap):
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 70)
        cap.set(cv2.CAP_PROP_CONTRAST, 30)
        cap.set(cv2.CAP_PROP_SATURATION, 30)
        cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 45)

    def cameraWorker(self, cap):
        while True:
            ret, frame = cap.read()
            self.imageQueueStartSignal.put(frame)
            self.imageQueueNumberDetector(frame)


class Window():

    def __init__(self):
        self.windowTrackbar = "trackbarWindow"
        self.windowWorkFrame = "workFrameWindow"
        self.windowOriginalFrame = "OriginalFrameWindow"

        self.threshTrackbar = "Threshold"
        self.hMaxTrackbar = "HMax"
        self.hMinTrackbar = "HMin"
        self.iteratorTrackbar = "iterator"
        self.kernelTrackbar = "Kernel"

    def getTrackbarValues(self, trackbar):
        return{
            self.threshTrackbar: cv2.getTrackbarPos(self.threshTrackbar, self.windowTrackbar),
            self.hMaxTrackbar: cv2.getTrackbarPos(self.hMaxTrackbar, self.windowTrackbar),
            self.hMinTrackbar: cv2.getTrackbarPos(self.hMinTrackbar, self.windowTrackbar),
            self.iteratorTrackbar: cv2.getTrackbarPos(self.iteratorTrackbar, self.windowTrackbar),
            self.kernelTrackbar: cv2.getTrackbarPos(self.kernelTrackbar, self.windowTrackbar)
        }.get(trackbar, 0)

    def createTrackbar(self):
        cv2.namedWindow(self.windowTrackbar)
        cv2.createTrackbar(self.threshTrackbar, self.windowTrackbar, 0, 255, nothing)
        cv2.createTrackbar(self.hMaxTrackbar, self.windowTrackbar, 0, 150, nothing)
        cv2.createTrackbar(self.hMinTrackbar, self.windowTrackbar, 0, 150, nothing)
        cv2.createTrackbar(self.iteratorTrackbar, self.windowTrackbar, 0, 255, nothing)
        cv2.createTrackbar(self.kernelTrackbar, self.windowTrackbar, 1, 30, nothing)