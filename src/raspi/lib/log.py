'''
Small logging abstraction to simplify usage

Usage:
-import log
'''
import logging

logger = logging.getLogger('SoulTrain')
logger.setLevel(logging.INFO)

#Write to file
fh = logging.FileHandler('SoulTrain.log')
fh.setLevel(logging.INFO)

#Write to stdout
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

#Formatting
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

def getLogger(component):
    '''
    get a logger instance
    '''
    return logging.getLogger(component)
