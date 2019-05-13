import time
from src.raspi.lib import log
import src.raspi.config.config as cfg

count = 0
limit = 5

logger = log.getLogger("SoulTrain.movement.phases.h_finished")

def method(middleware_data):
    logger.info("finished...")
    time.sleep(cfg.PHASE_DELAY)
    return ""
