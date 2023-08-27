import logging


class Logger:
    def load_logger(self):
        logger = logging.getLogger("simple_example")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        console = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s : %(message)s")
        console.setFormatter(formatter)
        logger.addHandler(console)
        return logger
