from statemachine import StateMachine, State
import cv2
from src.raspi.numberdetector.numberDetectionPython.detection import Detection
from src.raspi.numberdetector.numberDetectionPython.camera import Camera
from multiprocessing.pool import ThreadPool
import time


class SlaveStateMachine(StateMachine):

    def __init__(self, detection, cam):
        start = State('START', initial=True)
        startbereich = State('STARTBEREICH')
        runde1 = State('RUNDE1')
        runde2Langsam = State('RUNDE2_LANGSAM')
        runde2Schnell = State('RUNDE2_SCHNELL')
        runde3 = State('RUNDE3')
        ende = State('ENDE')

        self.startbefehl = start.to(startbereich)
        self.startsignalErkannt = startbereich.to(runde1)
        self.runde1StartSignalErkanntOhneNummer = runde1.to(runde2Langsam)
        self.runde1StartSignalErkanntMitNummer = runde1.to(runde2Schnell)
        self.stopSignalErkanntMitNummer = runde2Schnell.to(runde3)
        self.stopSignalErkanntOhneNummer = runde2Langsam.to(runde3)
        self.kleinTafelErkannt = runde3.to(ende)
        self.cam = cam
        self.pool = ThreadPool(process=3)
        self.detection = detection

    def on_enter_start(self):
        print("Neuer Zustand: START")
        self.cam.initCam(self.cam.cap)

    def on_enter_startbereich(self):
        print("Neuer Zustand: STARTBEREICH")
        self.pool.apply_async(self.cam.cameraWorker, self.cam.cap)
        self.pool.apply_async(self.detection.startSignalWorker)

    def on_enter_runde1(self):
        print("Neuer Zustand: RUNDE 1")
        self.pool.apply_async(self.detection.startPlateWorker)
        self.pool.apply_async(self.detection.startTeseractWorker)

    def on_enter_runde2Langsam(self):
        print("Neuer Zustand: RUNDE 2 LANGSAM")

    def on_enter_runde2Schnell(self):
        print("Neuer Zustand: RUNDE 2 SCHNELL")

    def on_enter_runde3(self):
        print("Neuer Zustand: RUNDE 3")

    def on_enter_ende(self):
        print("Neuer Zustand: ENDE")
