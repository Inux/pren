import src.raspi.config.config as cfg
from src.raspi.controlflow import mw_adapter_ctrlflow as mw
from src.raspi.lib import log

actual_distance = 0

logger = log.getLogger("SoulTrain.controlflow.phases.e_round_two")

def method(middleware_data):
    global actual_distance
    actual_distance = middleware_data['distance']

    if actual_distance >= cfg.DISTANCE_ROUND_TWO:
        logger.info("reached end of round two")
        return "" #success we finished second round

    if middleware_data['number'] is None:
        mw.send_move_cmd(cfg.SPEED_NUMBER_DETECTION_LIMIT)
        logger.debug("moving with number detection limit")
        return "moving with number detection limit"

    mw.send_move_cmd(cfg.SPEED_MAXIMAL_LIMIT)
    logger.debug("moving as fast as possible")
    return "moving as fast as possible"
