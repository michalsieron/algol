import os
import time


class Logger:
    def __init__(self, path):
        self._path = os.path.join(path, "algol.log")
        self._log_file = open(self._path, "a")

    def log(self, msg):
        self._log_file.write(f"{time.time()};{msg}\n")

    def close(self):
        self._log_file.close()
