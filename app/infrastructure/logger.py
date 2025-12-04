import logging

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
format = logging.Formatter("[%(asctime)s] [%(levelname)s]  %(name)s: %(message)s [%(req_id)s]")
handler.setFormatter(format)
logger.addHandler(handler)