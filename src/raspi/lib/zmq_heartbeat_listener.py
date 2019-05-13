#!/usr/bin/env python
import time
import zmq

import src.raspi.lib.log as log
from src.raspi.lib.singleton import Singleton
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.pb import heartbeat_pb2
from src.raspi.lib import heartbeat as hb
from src.raspi.config import config as cfg

logger = log.getLogger("SoulTrain.lib.heartbeat_listener.py")

# Sockets
reader_linedetector = zmq_socket.get_linedetector_reader()
reader_numberdetector = zmq_socket.get_numberdetector_reader()
reader_movement = zmq_socket.get_movement_reader()
reader_acoustic = zmq_socket.get_acoustic_reader()
reader_controlflow = zmq_socket.get_controlflow_reader()
reader_webapp = zmq_socket.get_webapp_reader()

class HeartBeatListener(metaclass=Singleton):
    '''
    Singleton instance to read HeartBeats
    - Automatically invalidates missing HeartBeats
    - Just read the dict by get_data()
    '''
    def __init__(self, *args, **kwargs):
        self.last_poll = None

        # Naming is important! Check __read_hb method!
        self.linedetector = hb.STATUS_FINISHED
        self.linedetector_last_scan = time.time()
        self.numberdetector = hb.STATUS_FINISHED
        self.numberdetector_last_scan = time.time()
        self.movement = hb.STATUS_FINISHED
        self.movement_last_scan = time.time()
        self.acoustic = hb.STATUS_FINISHED
        self.acoustic_last_scan = time.time()
        self.controlflow = hb.STATUS_FINISHED
        self.controlflow_last_scan = time.time()
        self.webapp = hb.STATUS_FINISHED
        self.webapp_last_scan = time.time()

        super().__init__(*args, **kwargs)

    def __name__(self):
        return repr(self)

    def get_linedetector(self):
        self.poll()
        return self.linedetector

    def get_numberdetector(self):
        self.poll()
        return self.numberdetector

    def get_movement(self):
        self.poll()
        return self.movement

    def get_acoustic(self):
        self.poll()
        return self.acoustic

    def get_controlflow(self):
        self.poll()
        return self.controlflow

    def get_webapp(self):
        self.poll()
        return self.webapp

    def get_data(self):
        '''
        get the actual heartbeat data
        '''
        self.poll()
        return dict(
            linedetector=self.linedetector,
            numberdetector=self.numberdetector,
            movement=self.movement,
            acoustic=self.acoustic,
            controlflow=self.controlflow,
            webapp=self.webapp
        )

    def poll(self):
        '''
        Check if new Heartbeats are available (updates all 15ms)
        '''
        if self.last_poll is None or ((time.time() - self.last_poll) > ((float(cfg.HB_INTERVAL)/1000))):
            self.__poll()
            self.last_poll = time.time()

    def __poll(self):  # Handle Heartbeat Messages
        self.__read_hb(hb.COMPONENT_LINEDETECTOR, self.linedetector_last_scan, reader_linedetector)
        self.__read_hb(hb.COMPONENT_NUMBERDETECTOR, self.numberdetector_last_scan, reader_numberdetector)
        self.__read_hb(hb.COMPONENT_ACOUSTIC, self.acoustic_last_scan, reader_acoustic)
        self.__read_hb(hb.COMPONENT_MOVEMENT, self.movement_last_scan, reader_movement)
        self.__read_hb(hb.COMPONENT_CONTROLFLOW, self.controlflow_last_scan, reader_controlflow)
        self.__read_hb(hb.COMPONENT_WEBAPP, self.webapp_last_scan, reader_webapp)

    def __read_hb(self, heartbeat, last_scan, socket):
        #getting value of member by name
        hb_status = getattr(self, heartbeat)

        if last_scan is None or ((time.time() - last_scan) > (float(cfg.HB_INVALIDATE_TIME)/1000)):
            hb_status = hb.STATUS_ERROR
            logger.error("set heartbeat from '%s' to status '%s'", heartbeat, hb_status)

        if socket.poll(timeout=0.05, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
            topic_and_data = socket.recv()
            topic = topic_and_data.split(b' ', 1)[0]
            dataraw = topic_and_data.split(b' ', 1)[1]

            if topic == zmq_topics.HEARTBEAT_TOPIC:
                # Try Parse HeartBeat
                rcv_hb = heartbeat_pb2.Heartbeat()
                rcv_hb.ParseFromString(dataraw)

                if rcv_hb is not None:
                    hb_status = rcv_hb.status
                    logger.debug("received heartbeat from '%s' with status '%s'", heartbeat, hb_status)

        #setting value of member by name
        setattr(self, heartbeat, hb_status)
        setattr(self, heartbeat+'_last_scan', time.time())
