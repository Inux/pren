import time

from src.raspi.config import config as cfg
from src.raspi.lib import heartbeat as hb
from src.raspi.lib import zmq_heartbeat_listener as hbl
from src.raspi.lib import log

logger = log.getLogger("SoulTrain.movement.phases.a_starting")


def method(middleware_data):
    hb_status = True

#   if hbl.HeartBeatListener().get_acoustic() not in hb.STATUS_RUNNING:
#        hb_status = False
#        logger.error("acoustic heartbeat is '" + hbl.HeartBeatListener().get_acoustic() + "' NOT '" + hb.STATUS_RUNNING + "'")
#        return "waiting for acoustic heartbeat..."

    if hbl.HeartBeatListener().get_controlflow() not in hb.STATUS_RUNNING:
        hb_status = False
        logger.error("controlflow heartbeat is '" + hbl.HeartBeatListener().get_controlflow() + "' NOT '" + hb.STATUS_RUNNING + "'")
        return "waiting for controlflow heartbeat..."

    if hbl.HeartBeatListener().get_linedetector() not in hb.STATUS_RUNNING:
        hb_status = False
        logger.error("linedetector heartbeat is '" + hbl.HeartBeatListener().get_linedetector() + "' NOT '" + hb.STATUS_RUNNING + "'")
        return "waiting for linedetector heartbeat..."

    if hbl.HeartBeatListener().get_movement() not in hb.STATUS_RUNNING:
        hb_status = False
        logger.error("movement heartbeat is '" + hbl.HeartBeatListener().get_movement() + "' NOT '" + hb.STATUS_RUNNING + "'")
        return "waiting for movement heartbeat..."

#   if hbl.HeartBeatListener().get_numberdetector() not in hb.STATUS_RUNNING:
#        hb_status = False
#        logger.error("numberdetector heartbeat is '" + hbl.HeartBeatListener().get_numberdetector() + "' NOT '" + hb.STATUS_RUNNING + "'")
#        return "waiting for numberdetector heartbeat..."

    if hbl.HeartBeatListener().get_webapp() not in hb.STATUS_RUNNING:
        hb_status = False
        return "waiting for webapp heartbeat..."

    time.sleep(cfg.PHASE_DELAY)

    return ""
