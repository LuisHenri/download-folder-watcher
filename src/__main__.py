import logging
import sys
import time
from pathlib import Path

from watchdog.observers import Observer

from downloadswatcher import FileEventHandler

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting Downloads Watcher")

    # TODO: Move observer to inside downloadswatcher.py
    observer = Observer()
    try:
        watchdog_handler = FileEventHandler()
        observer.schedule(
            watchdog_handler, str(Path.home() / "Downloads"), recursive=False
        )
        observer.start()

        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        raise


def setup_logger():
    """Setup default logging formatter and level."""
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    formatter = logging.Formatter("%(levelname)s %(asctime)s %(name)s: %(message)s")
    s_handler = logging.StreamHandler(sys.stdout)
    s_handler.setFormatter(formatter)

    params = {"level": logging.DEBUG, "handlers": [s_handler]}
    logging.basicConfig(**params)


if __name__ == "__main__":
    try:
        setup_logger()
        main()

    except KeyboardInterrupt:
        logger.info("Caught keyboard interrupt")
    except Exception as err:
        logger.error(err, exc_info=True)
    finally:
        logger.info("Exiting...")
