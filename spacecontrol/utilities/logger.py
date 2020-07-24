import logging


logger = logging.getLogger(__name__)
logger_format_fields = {
    'host': __file__
}


def setup_logger(is_verbose):
    verbosity_mapping = {
        False: logging.CRITICAL,
        True: logging.DEBUG
    }

    level = verbosity_mapping[is_verbose]

    global logger
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(host)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger = logging.LoggerAdapter(logger, logger_format_fields)