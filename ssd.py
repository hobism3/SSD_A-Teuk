import os
import sys

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

    def initialize_ssd_nand(self) -> None:
        with open(SSD_NAND_FILE_PATH, 'w', encoding='utf-8') as f:
            for i in range(100):
                f.writelines(f'{i:02d} {INITIAL_VALUE}\n')

    def initialize_ssd_output(self) -> None:
        with open(SSD_OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write('')

    def validate_address(self, input):
        if input is None:
            return False
        if not input.isdigit():
            return False
        if int(input) < 0 or int(input) > 99:
            return False
        return True

    def validate_value(self, input):
        if input is None:
            return False
        if not input.startswith('0x') and not input.startswith('0X'):
            return False
        if len(input) == 0 or len(input) > 10:
            return False
        try:
            int(input[2:], 16)
            return True
        except ValueError:
            return False

    def read(self, line_number):
        if not self.validate_address(line_number):
            self.report_error()
            return
        ret_value = ""
        with open(SSD_NAND_FILE_PATH, 'r') as f:
            for line in f:
                data = line.strip().split(' ')
                ind = int(data[0])

                if int(line_number) == ind:
                    ret_value = data[1]

        with open(SSD_OUTPUT_FILE_PATH, 'w') as f:
            f.write(f'{ret_value}')

    @staticmethod
    def report_error():
        with open(SSD_OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write('ERROR')

    def write(self, line_number, new_content):
        try:
            if not self.validate_address(line_number):
                raise InvalidInputError()
            if not self.validate_value(new_content):
                raise InvalidInputError()
            line_number = int(line_number)

            with open(SSD_NAND_FILE_PATH, encoding='utf-8') as f:
                lines = f.readlines()

            lines[line_number] = f'{line_number:02d} {new_content}\n'
            with open(SSD_NAND_FILE_PATH, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            self.initialize_ssd_output()
        except InvalidInputError:
            self.report_error()


def main():
    args = sys.argv[1:]
    try:
        if len(args) < 2:
            print('How to use:')
            print('  Write: python ssd.py W <adress> <value>')
            print('  Read: python ssd.py R <address>')
            raise InvalidInputError()

        mode = args[0].upper()

        if mode == 'W':
            if len(args) != 3:
                print('W need 3 arguments: W <address> <value>')
                raise InvalidInputError()
            address = args[1]
            value = args[2]

        elif mode == 'R':
            if len(args) != 2:
                print('R need 2 arguments: R <address>')
                raise InvalidInputError()
            address = args[1]
        else:
            print('Supported modes: W (write), R (read)')
            raise InvalidInputError()

        ssd = SSD()
        if mode == 'W':
            ssd.write(address, value)
        elif mode == 'R':
            ssd.read(address)
    except InvalidInputError:
        SSD.report_error()
        sys.exit(1)


if __name__ == '__main__':
    main()
