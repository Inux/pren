#!/usr/bin/env python
import time
import zmq

import src.raspi.lib.log as log
from src.raspi.lib.singleton import Singleton
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.pb import heartbeat_pb2
from src.raspi.lib import heartbeat as hb

logger = log.getLogger("SoulTrain.lib.heartbeat_listener.py")

# Sockets
reader_linedetector = zmq_socket.get_linedetector_reader()
reader_numberdetector = zmq_socket.get_numberdetector_reader()
reader_movement = zmq_socket.get_movement_reader()
reader_acoustic = zmq_socket.get_acoustic_reader()
reader_controlflow = zmq_socket.get_controlflow_reader()

MS_50 = 0.050 #50ms


class HeartBeatListener(metaclass=Singleton):
    '''
    Singleton instance to read HeartBeats
    - Automatically invalidates missing HeartBeats
    - Just read the dict by get_data()
    '''
    def __init__(self, *args, **kwargs):
        self.last_poll = None
        self.linedetector = hb.STATUS_ERROR
        self.linedetector_last_scan = None
        self.numberdetector = hb.STATUS_ERROR
        self.numberdetector_last_scan = None
        self.movement = hb.STATUS_ERROR
        self.movement_last_scan = None
        self.acoustic = hb.STATUS_ERROR
        self.acoustic_last_scan = None
        self.controlflow = hb.STATUS_ERROR
        self.controlflow_last_scan = None

        super().__init__(*args, **kwargs)

    def __name__(self):
        return repr(self)

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
            controlflow=self.controlflow
        )

    def poll(self):
        '''
        Check if new Heartbeats are available (updates all 15ms)
        '''
        if self.last_poll is None or ((time.perf_counter() - self.last_poll) > MS_50):
            self.__poll()
            self.last_poll = time.perf_counter()

    def __poll(self):  # Handle Heartbeat Messages
        self.__read_hb(self.linedetector, self.linedetector_last_scan, reader_linedetector)
        self.__read_hb(self.numberdetector, self.numberdetector_last_scan, reader_numberdetector)
        self.__read_hb(self.acoustic, self.acoustic_last_scan, reader_acoustic)
        self.__read_hb(self.movement, self.movement_last_scan, reader_movement)
        self.__read_hb(self.controlflow, self.controlflow_last_scan, reader_controlflow)

    def __read_hb(self, heartbeat, last_scan, socket):
        if last_scan is None or ((time.perf_counter() - last_scan) > MS_50):
            setattr(self, heartbeat, hb.STATUS_ERROR)

        if socket.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
            topic_and_data = socket.recv()
            topic = topic_and_data.split(b' ', 1)[0]
            dataraw = topic_and_data.split(b' ', 1)[1]

            if topic == zmq_topics.HEARTBEAT_TOPIC:
                # Try Parse HeartBeat
                heartbeat = heartbeat_pb2.Heartbeat()
                heartbeat.ParseFromString(dataraw)

                if heartbeat is not None:
                    logger.debug("received heartbeat from '%s' with status '%s'",
                                 heartbeat.component, heartbeat.status)
                    setattr(self, heartbeat, heartbeat.status)
