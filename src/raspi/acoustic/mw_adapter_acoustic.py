#!/usr/bin/env python
import os
import select
import zmq

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.pb import number_detection_pb2

logger = log.getLogger("SoulTrain.movement.mw_adapter_movement")

# Sockets
reader_number = zmq_socket.get_numberdetector_reader()
reader_web = zmq_socket.get_webapp_reader()

data = {}
data['number'] = 0

# Data Fields
def get_data():
    global data

    if reader_web.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = reader_web.recv()
        topic_and_data = topic_and_data.split(b' ')
        topic = topic_and_data.split(b' ', 1)[0]
        dataraw = topic_and_data.split(b' ', 1)[1]

        if topic == zmq_topics.NUMBER_DETECTOR_TOPIC:
            #Try parse number
            number = number_detection_pb2.NumberDetection
            number.ParseFromString(dataraw)

            if number is not None:
                logger.info("received acoustic command from Web. Number: '%s'", number.number)
                data['number'] = number.number

    if reader_number.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = reader_number.recv()
        topic_and_data = topic_and_data.split(b' ')
        topic = topic_and_data.split(b' ', 1)[0]
        dataraw = topic_and_data.split(b' ', 1)[1]

        if topic == zmq_topics.NUMBER_DETECTOR_TOPIC:
            #Try parse number
            number = number_detection_pb2.NumberDetection
            number.ParseFromString(dataraw)

            if number is not None:
                logger.info("received acoustic command from Numberdetector. Number: '%s'", number.number)
                data['number'] = number.number

    return data

