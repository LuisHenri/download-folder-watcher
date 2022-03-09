import logging
import os
from pathlib import Path

from watchdog.events import PatternMatchingEventHandler, FileModifiedEvent

logger = logging.getLogger(__name__)


class FileEventHandler(PatternMatchingEventHandler):

    _patterns_dict = {
        "*.png": "Pictures",
        "*.jpg": "Pictures",
        "*.jpeg": "Pictures",
        "*.txt": "Documents/TextFiles",
        "*.pdf": "Documents/PDFFiles",
        "*.doc": "Documents/WordFiles",
        "*.docx": "Documents/WordFiles",
        # TODO: Add more extensions
    }

    def __init__(self):
        super().__init__(patterns=self._patterns_dict.keys())
        logger.info("FileEventHandler initialized")

    def on_modified(self, event: FileModifiedEvent):
        logger.info(f"Found a new file: {event.src_path}")

        _, modified_file = os.path.split(os.path.abspath(event.src_path))
        modified_file_name, ext = os.path.splitext(modified_file)
        new_dest = str(Path.home() / self._patterns_dict["*" + ext])
        os.makedirs(new_dest, exist_ok=True)

        new_file_dest = f"{new_dest}/{modified_file}"
        file_num = 1
        while os.path.exists(new_file_dest):
            file_num += 1
            new_file_dest = f"{new_dest}/{modified_file_name} ({file_num}){ext}"

        try:
            os.rename(event.src_path, new_file_dest)
        except FileNotFoundError:
            pass
