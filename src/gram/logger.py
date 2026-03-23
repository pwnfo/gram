import sys
import logging

from typing import Any


class GramStreamHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord) -> Any:
        if record.levelno < logging.WARNING:
            self.stream = sys.stdout
        else:
            self.stream = sys.stderr
        super().emit(record)


def setup_logger() -> logging.Logger:
    log = logging.getLogger(__name__)

    handler = GramStreamHandler(sys.stdout)

    log.setLevel(logging.INFO)
    log.addHandler(handler)
    log.propagate = False

    return log


log = setup_logger()
