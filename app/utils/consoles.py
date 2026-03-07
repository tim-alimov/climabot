import logging
from rich.logging import RichHandler

def logging_initialize(DEBUG:bool = False) -> None:
    if DEBUG:
        log_level = logging.INFO
    else:
        log_level = logging.ERROR


    logging.basicConfig(
        level=log_level,
        format= "%(name)s - %(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )