import logging

logger = logging.getLogger("affiliations_logger")

logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.FileHandler("affiliations/affil.log")
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)