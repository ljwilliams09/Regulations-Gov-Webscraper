import logging

logger = logging.getLogger("affiliations_logger")

logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.FileHandler("affil.log")