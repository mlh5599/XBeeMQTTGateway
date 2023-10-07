import logging


def SetLogLevel(log_level):
    logging.debug(f'Setting log level to {log_level}')

    log_level_map = {
            'TRACE': logging.DEBUG,
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'NOTE': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'FATAL': logging.CRITICAL
        }

    log_level = log_level_map.get(log_level, logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(log_level)
