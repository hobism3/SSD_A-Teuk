import sys

INITIAL_VALUE = '00000000'
SSD_NAND_FILE_PATH = './ssd_nand.txt'
SSD_OUTPUT_FILE_PATH = './ssd_output.txt'


class SSD:
    def __init__(self):
        self.initialize_ssd_nand()

    def initialize_ssd_nand(self) -> None:
        f = open(SSD_NAND_FILE_PATH, 'w')
        for i in range(100):
            f.writelines(f'{i:02d} {INITIAL_VALUE}\n')
        f.close()

    def validate_address(self, input):
        if input is None:
            return False
        if not input.isdigit():
            return False
        num = int(input)
        if num < 0 or num > 99:
            return False
        return True

    def validate_value(self, input):
        if input is None:
            return False
        if len(input) != 8:
            return False
        return True

    def read(self):
        pass

    def report_error(self):
        with open(SSD_OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write('ERROR')

    def write(self, line_number, new_content):
        print('START WRITE')
        if not self.validate_address(line_number):
            self.report_error()
            return
        if not self.validate_value(new_content):
            self.report_error()
            return
        line_number = int(line_number)
        if new_content is None:
            self.report_error()
            return
        with open(SSD_NAND_FILE_PATH, encoding='utf-8') as f:
            lines = f.readlines()

        lines[line_number] = f'{line_number:02d} {new_content}\n'
        print(lines)
        with open(SSD_NAND_FILE_PATH, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f'Write Success! {line_number:02d}:{new_content}')
        with open(SSD_OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write('')


def main():
    args = sys.argv[1:]

    if len(args) < 2:
        print('How to use:')
        print('  Write: python ssd.py W <adress> <value>')
        print('  Read: python ssd.py R <address>')
        sys.exit(1)

    mode = args[0].upper()

    if mode == 'W':
        if len(args) != 3:
            print('W need 3 arguments: W <address> <value>')
            sys.exit(1)
        address = int(args[1])
        value = int(args[2], 8)  # 16진수 처리

    elif mode == 'R':
        if len(args) != 2:
            print('R need 2 arguments: R <address>')
            sys.exit(1)
        address = int(args[1])
    else:
        print('Supported modes: W (write), R (read)')
        sys.exit(1)

    ssd = SSD()
    if mode == 'W':
        ssd.write(address, f'{value:08x}')
    elif mode == 'R':
        ssd.read(address)


if __name__ == '__main__':
    main()
