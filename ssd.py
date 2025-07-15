import os
import sys
from abc import ABC, abstractmethod

INITIAL_VALUE = '0x00000000'
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
SSD_OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, 'ssd_output.txt')
SSD_NAND_FILE_PATH = os.path.join(OUTPUT_DIR, 'ssd_nand.txt')


class InvalidInputError(Exception):
    pass


class SSD:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not os.path.exists(SSD_NAND_FILE_PATH):
            print('Initialize')
            self.initialize_ssd_nand()
            self.initialize_ssd_output()

    @staticmethod
    def initialize_ssd_nand():
        with open(SSD_NAND_FILE_PATH, 'w', encoding='utf-8') as f:
            for i in range(100):
                f.write(f'{i:02d} {INITIAL_VALUE}\n')

    def initialize_ssd_output(self):
        with open(SSD_OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write('')

    def validate_address(self, input):
        if input is None or not input.isdigit():
            return False
        return 0 <= int(input) <= 99

    def validate_value(self, input):
        if input is None or len(input) != 10:
            return False
        if not input.startswith(('0x', '0X')):
            return False
        hex_part = input[2:]
        try:
            int(hex_part, 16)
            return True
        except ValueError:
            return False

    def read(self, line_number):
        ret_value = ''
        with open(SSD_NAND_FILE_PATH) as f:
            for line in f:
                data = line.strip().split(' ')
                ind = int(data[0])
                if int(line_number) == ind:
                    ret_value = data[1]

        with open(SSD_OUTPUT_FILE_PATH, 'w') as f:
            f.write(f'{ret_value}')

    def write(self, address, new_content):
        with open(SSD_NAND_FILE_PATH, encoding='utf-8') as f:
            lines = f.readlines()

        lines[address] = f'{address:02d} {new_content}\n'
        with open(SSD_NAND_FILE_PATH, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        self.initialize_ssd_output()

    def execute(self, mode, address, value=None):
        try:
            command = CommandFactory.create_command(
                [mode, address] + ([value] if value else [])
            )
            command.execute()
        except InvalidInputError:
            self.report_error()

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
            raise InvalidInputError()
        self.ssd.read(int(self.address))


class WriteCommand(Command):
    def __init__(self, ssd, address, value):
        self.ssd = ssd
        self.address = address
        self.value = value

    def execute(self):
        if not self.ssd.validate_address(self.address) or not self.ssd.validate_value(
            self.value
        ):
            raise InvalidInputError()
        self.ssd.write(int(self.address), self.value)


class CommandFactory:
    @staticmethod
    def create_command(args):
        if len(args) < 2:
            raise InvalidInputError('Insufficient arguments')

        mode = args[0].upper()
        address = args[1]
        value = args[2] if len(args) > 2 else None

        ssd = SSD()

        if mode == 'W':
            if value is None:
                raise InvalidInputError('Write needs a value')
            return WriteCommand(ssd, address, value)

        elif mode == 'R':
            return ReadCommand(ssd, address)

        else:
            raise InvalidInputError('Invalid mode')

    def execute(self, param, param1, param2=None):
        pass


def main():
    args = sys.argv[1:]
    try:
        command = CommandFactory.create_command(args)
        command.execute()
    except InvalidInputError:
        SSD.report_error()
        sys.exit(1)


if __name__ == '__main__':
    main()
