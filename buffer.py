import os
from pathlib import Path

BUFFER_DIR_NAME = 'buffer'
BUFFER_DIR = f'{os.path.dirname(os.path.abspath(__file__))}/{BUFFER_DIR_NAME}'

class Buffer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._create_directory(BUFFER_DIR)
        if os.listdir(BUFFER_DIR) == []:
            self._create_file(BUFFER_DIR)

    def _create_file(self, dir):
        for i in range(1, 6):
            Path(f"{dir}/{i}_empty").touch()

    def _create_directory(self, dir):
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
        except OSError:
            print("Creation of the directory %s failed" % dir)

    def buffer_file_read(self) -> list:
        ...

    def buffer_file_write(self, lst):
        ...

    def _write(self, address, new_content):
        ...

    def _read(self, address):
        ...

    def _erase(self):
        ...
