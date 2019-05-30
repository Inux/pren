import time
from src.raspi.lib import log

import src.raspi.controlflow.mw_adapter_ctrlflow as mw
import src.raspi.config.config as cfg

count = 0
limit = 5

logger = log.getLogger("SoulTrain.controlflow.phases.h_finished")

time_waited = 0.0

def method(middleware_data):
    global time_waited

    if time_waited <= 0.0: #only once sending commands
        mw.send_move_cmd(0)
        mw.send_crane_cmd(0)

    time_waited = time_waited + 0.1
    time.sleep(0.1)

    if time_waited < cfg.PHASE_DELAY:
        return "delaying a bit...."

    logger.info("finished...")
    return ""
