import logging

logger = logging.getLogger("api_logger")

logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.FileHandler("dockets/docket.log")
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
