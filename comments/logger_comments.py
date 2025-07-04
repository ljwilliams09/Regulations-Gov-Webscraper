import logging

logger = logging.getLogger("api_logger")
with open("config.json", 'r') as c:
    config = c.json()

logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.FileHandler(f"{config["year"]}.log")
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
