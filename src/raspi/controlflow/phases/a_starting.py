import time

from src.raspi.lib import heartbeat as hb
from src.raspi.lib import zmq_heartbeat_listener as hbl

count = 0
limit = 5

def method(middleware_data):
    hb_status = True
    #hb_status = hb_status and (hbl.HeartBeatListener().get_acoustic() in hb.STATUS_RUNNING)
    hb_status = hb_status and (hbl.HeartBeatListener().get_controlflow() in hb.STATUS_RUNNING)
    hb_status = hb_status and (hbl.HeartBeatListener().get_linedetector() in hb.STATUS_RUNNING)
    hb_status = hb_status and (hbl.HeartBeatListener().get_movement() in hb.STATUS_RUNNING)
    #hb_status = hb_status and (hbl.HeartBeatListener().get_numberdetector() in hb.STATUS_RUNNING)
    hb_status = hb_status and (hbl.HeartBeatListener().get_webapp() in hb.STATUS_RUNNING)

    if hb_status is False:
        return "waiting for heartbeats..."

    global count
    if count < limit:
        count = count + 1
        time.sleep(0.5)
        return "'" + str(count) + "' < '" + str(limit) + "'"

    count = 0
    return ""
