import os

from logger import Logger
from pathlib import Path

MAX_BUFFER_SIZE = 5
BUFFER_DIR_NAME = 'buffer'
BUFFER_DIR = f'{os.path.dirname(os.path.abspath(__file__))}/{BUFFER_DIR_NAME}'

class Buffer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger()
        self._create_directory(BUFFER_DIR)
        if len(os.listdir(BUFFER_DIR)) < MAX_BUFFER_SIZE:
            self._create_file(BUFFER_DIR)

    def _create_file(self, dir):
        for i in range(MAX_BUFFER_SIZE):
            Path(f'{dir}/{i + 1}_empty').touch()

    def _create_directory(self, dir):
        try:
            os.makedirs(dir, exist_ok=True)
        except OSError:
            self.logger.error(f'Creation of the directory {dir} failed')

    def buffer_file_read(self) -> list:
        return sorted(os.listdir('buffer'))

    def buffer_file_write(self, lst):
        file_list = self.buffer_file_read()
        for i, file in enumerate(lst):
            before_file_path = f'{BUFFER_DIR}\{file_list[i]}'
            after_file_path = f'{BUFFER_DIR}\{file}'
            try:
                os.rename(before_file_path, after_file_path)
            except OSError as e:
                self.logger.error(f'Error during changing buffer {before_file_path} to {after_file_path}')

    def _write(self, address, new_content): ...

    def _read(self, address): ...

    def _erase(self, address, size): ...
