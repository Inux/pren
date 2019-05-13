import src.raspi.config.config as cfg
from src.raspi.controlflow import mw_adapter_ctrlflow as mw
from src.raspi.lib import log

actual_distance = 0

logger = log.getLogger("SoulTrain.movement.phases.f_find_stop")

def method(middleware_data):
    global actual_distance
    actual_distance = middleware_data['distance']

    if actual_distance >= ((cfg.DISTANCE_ROUND_MM*2) + cfg.DISTANCE_STOP_MAX):
        mw.send_move_cmd(0)
        logger.error("reached end but not at correct stop...")
        return ""

    if middleware_data['number'] is not None and middleware_data['number'] == 0:
        mw.send_move_cmd(0)
        logger.info("reached end at correct stop")
        return ""

    mw.send_move_cmd(cfg.SPEED_STOP_SEARCH)
    logger.debug("searching stop...")
    return "searching stop..."
