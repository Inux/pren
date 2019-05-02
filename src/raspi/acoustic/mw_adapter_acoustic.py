#!/usr/bin/env python
import os
import select
import zmq

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.pb import number_detection_pb2
from src.raspi.pb import acoustic_command_pb2

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
        logger.info("topic_and_data: %s", str(topic_and_data))
        topic = topic_and_data.split(b' ', 1)[0]
        logger.info("topic: %s", str(topic))
        dataraw = topic_and_data.split(b' ', 1)[1]
        logger.info("dataraw: %s", str(dataraw))

        if topic == zmq_topics.ACOUSTIC_TOPIC:
            #Try parse number
            acoustic_cmd = acoustic_command_pb2.AcousticCommand()
            acoustic_cmd.ParseFromString(dataraw)

            if acoustic_cmd is not None:
                logger.info("received acoustic command from Web. Number: '%s'", acoustic_cmd.number)
                data['number'] = acoustic_cmd.number

    if reader_number.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = reader_number.recv()
        logger.info("topic_and_data: %s", str(topic_and_data))
        topic = topic_and_data.split(b' ', 1)[0]
        logger.info("topic: %s", str(topic))
        dataraw = topic_and_data.split(b' ', 1)[1]
        logger.info("dataraw: %s", str(dataraw))

        if topic == zmq_topics.NUMBER_DETECTOR_TOPIC:
            #Try parse number
            number = number_detection_pb2.NumberDetection()
            number.ParseFromString(dataraw)

            if number is not None:
                logger.info("received acoustic command from Numberdetector. Number: '%s'", number.number)
                data['number'] = number.number

    return data

