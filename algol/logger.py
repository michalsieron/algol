import os
import time


class Logger:
    """Helper class for logging events"""

    def __init__(self, path: str, name: str):
        self._path = os.path.join(path, name)
        self._log_file = open(self._path, "a")

    def log(self, msg: str):
        """Use this method to log given message"""
        self._log_file.write(f"{time.time()};{msg}\n")

    def close(self):
        self._log_file.close()
