import time

from src.raspi.controlflow import mw_adapter_ctrlflow as mw
from src.raspi.config import config as cfg
from src.raspi.lib import log

logger = log.getLogger("SoulTrain.controlflow.phases.b_find_cube")

def method(middleware_data):
    if 'cube' in middleware_data.keys() and int(middleware_data['cube']) == int(1):
        logger.info("found cube")
        mw.send_move_cmd(0)
        return ""

    logger.debug("searching for cube...")
    mw.send_move_cmd(cfg.SPEED_CUBE_SEARCH)
    return "searching cube..."
