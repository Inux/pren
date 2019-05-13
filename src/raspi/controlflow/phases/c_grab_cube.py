import time

from src.raspi.controlflow import mw_adapter_ctrlflow as mw
from src.raspi.config import config as cfg
from src.raspi.lib import log

crane_sent = False
time_waited = 0

logger = log.getLogger("SoulTrain.movement.phases.c_grab_cube")

def method(middleware_data):
    global crane_sent
    global time_waited

    if 'crane' in middleware_data.keys() and int(middleware_data['crane']) == 1 and int(time_waited) >= cfg.CRANE_WAIT_TIME:
        crane_sent = False
        time_waited = 0
        mw.send_crane_cmd(0)
        logger.info("grabbed cube - ready to go")
        return ""

    if crane_sent is False:
        crane_sent = True
        mw.send_crane_cmd(1)
        time_waited = time_waited + cfg.CRANE_POLL_TIME
        time.sleep(cfg.CRANE_POLL_TIME)
        logger.info("sent crane command to movement")
        return "sent crane cmd..."

    time_waited = time_waited + cfg.CRANE_POLL_TIME
    time.sleep(cfg.CRANE_POLL_TIME)

    logger.debug("waiting for crane (" + str(time_waited) + "s)")
    return "waiting for crane... (" + str(time_waited) + "s)"
