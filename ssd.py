from abc import ABC, abstractmethod
from functools import wraps
import os
import sys

from filelock import FileLock

from ssd_tool.buffer import Buffer
from ssd_tool.logger import Logger

INITIAL_VALUE = '0x00000000'
SSD_NAND_SIZE = 100
VALID_VALUE_SIZE = 10
EMPTY = 'empty'
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
SSD_OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, 'ssd_output.txt')
SSD_NAND_FILE_PATH = os.path.join(OUTPUT_DIR, 'ssd_nand.txt')
LOCK_FILE_PATH = os.path.join(OUTPUT_DIR, 'ssd_tool.lock')


def file_lock_decorator(lock_path):
    lock = FileLock(lock_path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                result = func(*args, **kwargs)
                return result

        return wrapper

    return decorator


class InvalidInputError(Exception):
    pass


class SSD:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger()
        self._buffer = Buffer()
        if self._buffer.buffer_length == 5:
            self.logger.info('Buffer is full. Flush buffer.')
            self.flush()
        if not os.path.exists(SSD_NAND_FILE_PATH):
            self.logger.info('Initialize ssd_nand.txt, ssd_output.txt')
            self.initialize_ssd_nand()
            self.initialize_ssd_output()

    @staticmethod
    def initialize_ssd_nand():
        with open(SSD_NAND_FILE_PATH, 'w', encoding='utf-8') as f:
            for i in range(SSD_NAND_SIZE):
                f.write(f'{i:02d} {INITIAL_VALUE}\n')

    @staticmethod
    def initialize_ssd_output():
        with open(SSD_OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write('')

    @staticmethod
    def validate_address(input_val):
        if input_val is None or not input_val.isdigit():
            return False
        return 0 <= int(input_val) <= SSD_NAND_SIZE - 1

    @staticmethod
    def validate_value(input_val):
        if input_val is None or len(input_val) != VALID_VALUE_SIZE:
            return False
        if not input_val.startswith(('0x', '0X')):
            return False
        hex_part = input_val[2:]
        try:
            int(hex_part, 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_size(address, input_val):
        if input_val is None or not input_val.isdigit():
            return False
        if int(address) + int(input_val) > SSD_NAND_SIZE:
            return False
        return 1 <= int(input_val) <= VALID_VALUE_SIZE

    def read(self, address):
        is_read_buf, ret_value = self._buffer.read(int(address))
        if not is_read_buf:
            with open(SSD_NAND_FILE_PATH) as f:
                lines = f.readlines()
                ret_value = lines[int(address)].strip().split(' ')[1]
        with open(SSD_OUTPUT_FILE_PATH, 'w') as f:
            f.write(f'{ret_value}')
        self.logger.info(f'Read complete: {address:02d}: {ret_value}')

    def _write(self, address, new_content):
        with open(SSD_NAND_FILE_PATH, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            lines[address] = f'{address:02d} {new_content}\n'
            f.seek(0)
            f.writelines(lines)
            f.truncate()

        self.initialize_ssd_output()
        self.logger.info(f'Write complete: {address:02d}: {new_content}')

    def _erase(self, address, size):
        with open(SSD_NAND_FILE_PATH, 'r+', encoding='utf-8') as f:
            lines = f.readlines()

            for i in range(address, address + size):
                lines[i] = f'{i:02d} {INITIAL_VALUE}\n'
            f.seek(0)
            f.writelines(lines)
            f.truncate()

        self.initialize_ssd_output()
        self.logger.info(f'Erase complete: {address:02d} to {address + size:02d}')

    def flush(self):
        self.logger.info('Flush Start')
        buffer_list = self._buffer._buffer_file_read_as_list()
        for buffed_command in buffer_list:
            if EMPTY in buffed_command:
                break
            if buffed_command[0] == 'W':
                self._write(buffed_command[1], buffed_command[2])
            elif buffed_command[0] == 'E':
                self._erase(buffed_command[1], buffed_command[2])
            elif buffed_command[0] == 'R':
                self.read(buffed_command[1])

        self._buffer.buffer_clear()
        self.logger.info('Flush complete')

    def buf_write(self, address, new_content):
        self._buffer.buffer_arrange(
            'W', address, new_content, self._buffer.buffer_length
        )
        self._buffer.buffer_file_write()
        self.initialize_ssd_output()
        self.logger.info(f'Write complete: {address:02d}: {new_content}')

    def buf_erase(self, address, size):
        self._buffer.buffer_arrange('E', address, size, self._buffer.buffer_length)
        self._buffer.buffer_file_write()
        self.initialize_ssd_output()
        self.logger.info(f'Erase complete: {address:02d}: {size:02d}')

    def execute_test(self, args):
        self.execute_test_log(args)
        try:
            command = CommandFactory.create_command(args)
            command.execute()
        except InvalidInputError as e:
            self.report_error()
            self.logger.error(e)

    def execute_test_log(self, args):
        mode = args[0]
        address = args[1] if len(args) > 1 and args[1] else ''
        value = args[2] if len(args) > 2 and args[2] else ''
        self.logger.info(f'Execute command: {mode} {address} {value}')

    @staticmethod
    def report_error():
        with open(SSD_OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write('ERROR')


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class ReadCommand(Command):
    def __init__(self, ssd, address):
        self.ssd = ssd
        self.address = address

    def execute(self):
        if not self.ssd.validate_address(self.address):
            raise InvalidInputError('Address validation failed')
        self.ssd.read(int(self.address))


class WriteCommand(Command):
    def __init__(self, ssd, address, value):
        self.ssd = ssd
        self.address = address
        self.value = value

    @file_lock_decorator(LOCK_FILE_PATH)
    def execute(self):
        if not self.ssd.validate_address(self.address) or not self.ssd.validate_value(
            self.value
        ):
            raise InvalidInputError('Address validation failed')
        self.ssd.buf_write(int(self.address), self.value)


class EraseCommand(Command):
    def __init__(self, ssd, address, size):
        self.ssd = ssd
        self.address = address
        self.size = size

    @file_lock_decorator(LOCK_FILE_PATH)
    def execute(self):
        if not self.ssd.validate_address(self.address) or not self.ssd.validate_size(
            self.address, self.size
        ):
            raise InvalidInputError('Address validation failed')
        self.ssd.buf_erase(int(self.address), int(self.size))


class FlushCommand(Command):
    def __init__(self, ssd):
        self.ssd = ssd

    @file_lock_decorator(LOCK_FILE_PATH)
    def execute(self):
        self.ssd.flush()


class CommandFactory:
    MODES = {
        'R': {'command': ReadCommand, 'args_count': 1},
        'W': {'command': WriteCommand, 'args_count': 2},
        'E': {'command': EraseCommand, 'args_count': 2},
        'F': {'command': FlushCommand, 'args_count': 0},
    }

    @staticmethod
    def create_command(args):
        if not args:
            raise InvalidInputError('No arguments provided')

        mode = args[0].upper()
        ssd = SSD()

        if mode not in CommandFactory.MODES:
            raise InvalidInputError(
                f'Invalid mode: {mode}. Supported modes are {", ".join(CommandFactory.MODES.keys())}.'
            )

        if CommandFactory.MODES[mode]['args_count'] != len(args) - 1:
            raise InvalidInputError(
                f'{mode} only accepts {CommandFactory.MODES[mode]["args_count"]} arguments'
            )

        command = CommandFactory.MODES[mode]['command']
        return command(ssd, *args[1:])


def main():
    args = sys.argv[1:]
    try:
        command = CommandFactory.create_command(args)
        command.execute()
    except InvalidInputError:
        SSD.report_error()
        sys.exit(0)


if __name__ == '__main__':
    main()
