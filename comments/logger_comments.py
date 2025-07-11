import logging
import json

logger = logging.getLogger("api_logger")
with open("config.json", 'r') as c:
    config = json.load(c)
year = 2024

logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.FileHandler(f"{config['output_path']}log/{year}.log")
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
