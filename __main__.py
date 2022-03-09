import logging
import sys
import time
from pathlib import Path

from dirwatcher import DirWatcher, FileEventHandler

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting Downloads Watcher")

    handler = FileEventHandler()
    downloads_watcher = DirWatcher(str(Path.home() / "Downloads"), handler)
    try:
        downloads_watcher.start()
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        downloads_watcher.stop()
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
    logging.getLogger("watchdog.observers.inotify_buffer").setLevel(logging.INFO)


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
