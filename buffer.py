import os
from pathlib import Path

from logger import Logger

MAX_BUFFER_SIZE = 5
ERASE_MAX_RANGE = 10
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
        self.buffer = self.buffer_file_read_as_list()
        self.logger.info(self.buffer)

    def _create_file(self, dir):
        for i in range(MAX_BUFFER_SIZE):
            Path(f'{dir}/{i + 1}_empty').touch()

    def _create_directory(self, dir):
        try:
            os.makedirs(dir, exist_ok=True)
        except OSError:
            self.logger.error(f'Creation of the directory {dir} failed')

    def buffer_file_read_as_list(self) -> list:
        list = [file.split('_')[1:] for file in sorted(os.listdir('buffer'))]
        for i in range(len(list)):
            if list[i][0] == 'empty':
                continue
            list[i][1] = int(list[i][1])
            if list[i][0] == 'E':
                list[i][2] = int(list[i][2])
                continue
        return list

    def buffer_file_read(self) -> list:
        return sorted(os.listdir('buffer'))

    def buffer_file_write(self):
        file_list = self.buffer_file_read()
        self.logger.info(f'write: {file_list}, self.buffer: {self.buffer}')
        for i in range(len(file_list)):
            before_file_path = rf'{BUFFER_DIR}\{file_list[i]}'
            if self.buffer[i][0] == 'empty':
                after_file_path = rf'{BUFFER_DIR}\{i + 1}_empty'
            else:
                after_file_path = rf'{BUFFER_DIR}\{i + 1}_{self.buffer[i][0]}_{self.buffer[i][1]}_{self.buffer[i][2]}'
            try:
                print(before_file_path, after_file_path)
                os.rename(before_file_path, after_file_path)
            except OSError:
                self.logger.error(
                    f'Error during changing buffer {before_file_path} to {after_file_path}'
                )

    def buffer_clear(self):
        file_list = self.buffer_file_read()
        for i in range(MAX_BUFFER_SIZE):
            before_file_path = rf'{BUFFER_DIR}\{file_list[i]}'
            after_file_path = rf'{BUFFER_DIR}\{i + 1}_empty'
            try:
                os.rename(before_file_path, after_file_path)
            except OSError:
                self.logger.error(
                    f'Error during changing buffer {before_file_path} to {after_file_path}'
                )

    def _write(self, address, new_content):
        self.buffer_arrange('W', address, new_content, self._get_buffer_length())
        self.buffer_file_write()

    def _read(self, address) -> (bool, str):
        for buf in self.buffer:
            if buf[0] == 'empty':
                continue
            if buf[0] == 'W' and buf[1] == address:
                return True, buf[2]
            if buf[0] == 'E' and buf[1] <= address < buf[1] + buf[2]:
                return True, '0x00000000'
        return False, ''

    def _erase(self, address, size):
        self.buffer_arrange('E', address, size, self._get_buffer_length())
        self.buffer_file_write()

    def _add_buffer(self, seq, mode, address, value):
        self.buffer[seq] = [mode, address, value]

    def _remove_buffer(self, seq):
        self.logger.info(f'Remove buffer {seq}')
        self.buffer[seq] = ['empty']

    def _can_merge_ranges(self, addr1, len1, addr2, len2):
        self.logger.info(f'Can merge ranges?: {addr1} {len1} {addr2} {len2}')
        range1 = set(range(addr1, addr1 + len1))
        range2 = set(range(addr2, addr2 + len2))
        merged = sorted(range1 | range2)

        if merged[-1] - merged[0] + 1 == len(merged):
            merged_start = merged[0]
            merged_len = len(merged)
            if merged_len > ERASE_MAX_RANGE:
                return False, [
                    (merged[0], merged_len - ERASE_MAX_RANGE),
                    (merged[-ERASE_MAX_RANGE], ERASE_MAX_RANGE),
                ]
            return True, (merged_start, merged_len)
        return False, None

    def _reduce_erase_buffer(self, i, param1):
        buf = self.buffer[i]
        start, length = int(buf[1]), int(buf[2])

        if start == param1:
            self.logger.info(f'Erase range(F) reduced {start}: {length}')
            buf[1] = param1 + 1
            buf[2] = length - 1
            if buf[2] == 0:
                self.logger.info(f'Erase is useless now. Remove buffer {i}')
                self._remove_buffer(i)
                return True
        elif start + length - 1 == param1:
            self.logger.info(f'Erase range(R) reduced {start}: {length}')
            buf[2] = length - 1
            if buf[2] == 0:
                self.logger.info(f'Erase is useless now. Remove buffer {i}')
                self._remove_buffer(i)
                return True
        return False

    def buffer_arrange(self, mode, param1, param2, seq):
        self.logger.info(f'Buffer Arrange: {mode} {param1} {param2}, {seq}')
        flag_add_buffer = True

        self._remove_buffer(seq)

        if mode == 'W':
            for i in range(seq, -1, -1):
                buf = self.buffer[i]
                if buf[0] == 'W' and buf[1] == param1:
                    self._remove_buffer(i)
                    self._sort_buffer()
                    seq -= 1
                    break
                if buf[0] == 'E':
                    erased = self._reduce_erase_buffer(i, param1)
                    if erased:
                        self._sort_buffer()
                        seq -= 1
                        break
        elif mode == 'E':
            for i in range(seq, -1, -1):
                buf = self.buffer[i]
                if buf[0] == 'W' and param1 <= buf[1] < param1 + param2:
                    self.logger.info(f'Write is useless now. Remove buffer {i}')
                    self._remove_buffer(i)
                    self._sort_buffer()
                    seq -= 1
                elif buf[0] == 'E':
                    can_merge, merged_range = self._can_merge_ranges(
                        buf[1], buf[2], param1, param2
                    )
                    if can_merge:
                        self.logger.info(f'Buffer {i} can be merged.')
                        self._add_buffer(i, 'E', merged_range[0], merged_range[1])
                        self._sort_buffer()
                        flag_add_buffer = False
                    elif merged_range is not None:
                        self.logger.info(
                            f'Buffer Rearranged. merged_range: {merged_range}'
                        )
                        self._add_buffer(i, 'E', merged_range[0][0], merged_range[0][1])
                        param1, param2 = merged_range[1][0], merged_range[1][1]

        if flag_add_buffer:
            self.logger.info(f'Add buffer {seq} {mode} {param1} {param2}')
            self._add_buffer(seq, mode, param1, param2)

        self.logger.info(self.buffer)

        if seq > 0:
            self.buffer_arrange(
                self.buffer[seq - 1][0],
                self.buffer[seq - 1][1],
                self.buffer[seq - 1][2],
                seq - 1,
            )

    def _sort_buffer(self):
        non_empty = [x for x in self.buffer if x != ['empty']]
        empty = [x for x in self.buffer if x == ['empty']]
        self.buffer = non_empty + empty

    def _get_buffer_length(self):
        non_empty = [x for x in self.buffer if x != ['empty']]
        return len(non_empty)
