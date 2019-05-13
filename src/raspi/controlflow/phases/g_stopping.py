import time

import src.raspi.controlflow.mw_adapter_ctrlflow as mw
import src.raspi.config.config as cfg
from src.raspi.lib import log

logger = log.getLogger("SoulTrain.movement.phases.g_stopping")

def method(middleware_data):
    logger.info("stopping...")
    mw.send_move_cmd(0)
    mw.send_crane_cmd(0)
    time.sleep(cfg.PHASE_DELAY)
    return ""
