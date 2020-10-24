import logging


def getlogger(mod_name:str, filepath:str):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # 单独设置
    logger.propagate = False
    handler = logging.FileHandler(filepath)
    fmter = logging.Formatter('%(asctime)s [%(name)s %(funcName)s] %(message)s')
    handler.setFormatter(fmter)
    logger.addHandler(handler)
    return logger


