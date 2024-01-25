"""custom logger

Returns:
    _type_: _description_
"""
import logging
from logging import Logger
from pathlib import Path

FILE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
TERM_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class CustomFormatterTerminal(logging.Formatter):
  """
  Custom logger to print colored text on terminal
  """
  HEADER = '\033[95m'
  DEBUG = '\033[6;30;44m'
  WARNING = '\033[0;30;43m'
  INFO = '\033[6;30;47m'
  FAIL = '\033[0;30;41m'
  ENDC = '\033[0m'

  # source for colouring: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
  FORMATS = {
    logging.DEBUG: DEBUG + TERM_FORMAT + ENDC,
    logging.INFO: INFO + TERM_FORMAT + ENDC,
    logging.WARNING: WARNING + TERM_FORMAT + ENDC,
    logging.ERROR: FAIL + TERM_FORMAT + ENDC,
    logging.CRITICAL: FAIL + TERM_FORMAT + ENDC
  }

  def format(self, record):
    log_fmt = self.FORMATS.get(record.levelno)
    formatter = logging.Formatter(log_fmt)
    return formatter.format(record)

# create logger
logger = logging.getLogger("log_data")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatterTerminal())

logger.addHandler(ch)

def set_file_handler(logger: Logger, path_to_save: Path):
  file_handler = logging.FileHandler(path_to_save/ "log_data.log")
  file_handler.setLevel(logging.DEBUG)
  logFormatter = logging.Formatter(fmt=FILE_FORMAT)
  file_handler.setFormatter(logFormatter)
  logger.addHandler(file_handler)

set_file_handler(logger, Path("logs"))