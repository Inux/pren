import time

from src.raspi.controlflow import mw_adapter_ctrlflow as mw
from src.raspi.config import config as cfg

def method(middleware_data):
    if 'cube' in middleware_data.keys() and int(middleware_data['cube']) == int(1):
        mw.send_move_cmd(0)
        return ""

    mw.send_move_cmd(cfg.SPEED_CUBE_SEARCH)
    return "searching cube..."
