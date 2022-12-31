import logging
import os
from pathlib import Path

from watchdog.events import FileModifiedEvent, PatternMatchingEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)


class FileEventHandler(PatternMatchingEventHandler):
    """Subclass of `watchdog.events.PatternMatchingEventHandler` to handle file
    system events.

    The user can `copy and paste`, `move` or `edit` files/folders inside the
    directory that is being monitored. An event will then be handled only when the event
    path matches the given pattern.

    NOTE: the user is NOT encouraged to `move` or `copy and paste` multiple files
        at the same time.
    """

    def __init__(self, file_patterns: dict):
        """Initialize the new class instance.

        :param file_patterns: dictionary of file patterns and their destination
        """
        self.inv_file_patterns = {
            pat: dest for dest, pat_list in file_patterns.items() for pat in pat_list
        }
        super().__init__(
            patterns=[pat for pat in self.inv_file_patterns.keys()],
            ignore_directories=True,
        )

        logger.info("FileEventHandler initialized")

    def on_modified(self, event: FileModifiedEvent):
        """Called when a modified event is triggered.

        Creating a file also triggers a modified event – that's why we don't
        need the on_created method.

        :param event: event object representing the file system event
        """
        logger.info(f"Found a new file: {event.src_path}")

        _, modified_file = os.path.split(os.path.abspath(event.src_path))
        modified_file_name, ext = os.path.splitext(modified_file)
        new_dest = str(Path.home() / self.inv_file_patterns["*" + ext])
        os.makedirs(new_dest, exist_ok=True)

        new_file_dest = f"{new_dest}/{modified_file}"
        file_num = 1
        while os.path.exists(new_file_dest):
            file_num += 1
            new_file_dest = f"{new_dest}/{modified_file_name} ({file_num}){ext}"

        try:
            os.rename(event.src_path, new_file_dest)
        except FileNotFoundError as err:
            logger.debug(err)


class DirWatcher:
    """Thread class to monitor file system events."""

    def __init__(self, watch_path: str, handler: FileEventHandler):
        """Initialize the new class instance.

        :param watch_path: path to the directory to be monitored
        :param handler: filesystem event handler
        """
        if not os.path.isdir(watch_path):
            raise NotADirectoryError(f"{watch_path} is not a directory")
        self.__src_path = watch_path
        self.__event_handler = handler
        self.__event_observer = Observer()

    def start(self):
        """Start the observer thread and wait for it to generate events without
        blocking the main thread.
        """
        self.__schedule()
        self.__event_observer.start()
        logger.info(f"Watching {self.__src_path} folder")

    def stop(self):
        """Signal the thread to stop and wait until the thread terminates."""
        self.__event_observer.stop()
        self.__event_observer.join()

    def is_running(self) -> bool:
        """Return whether the thread is alive.

        :return: True if it is running, False otherwise
        """
        return self.__event_observer.is_alive()

    def __schedule(self):
        """Schedule monitoring the path with the event handler."""
        self.__event_observer.schedule(
            self.__event_handler, self.__src_path, recursive=False
        )
