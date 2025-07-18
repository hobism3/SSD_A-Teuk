import os
import subprocess

import pytest

from ssd import SSD, SSD_NAND_FILE_PATH, SSD_OUTPUT_FILE_PATH

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SSD_PATH = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..', 'ssd.py'))

COMMAND_PREFIX = f'python {SSD_PATH}'

ERROR = 'ERROR'
SSD_NAND_FILE_PATH = SSD_NAND_FILE_PATH
SSD_OUTPUT_FILE_PATH = SSD_OUTPUT_FILE_PATH
VALID_ADDRESS = '00'
INVALID_ADDRESS = '100'
INITIAL_VALUE = '0x00000000'
VALID_VALUE = '0x00000001'
VALID_SIZE = '5'


def run_direct(ssd_instance):
    def runner(*args):
        ssd_instance.execute_test(args)
        ssd_instance.execute_test('F')

    return runner


def run_cli(ssd_instance):
    def runner(*args):
        cli_args = [str(arg) for arg in args]
        full_command = f'{COMMAND_PREFIX} {cli_args[0]} {" ".join(cli_args[1:])}'
        subprocess.run(full_command, shell=True, check=True)
        subprocess.run(f'{COMMAND_PREFIX} F', shell=True, check=True)

    return runner


def run_direct_wo_flush(ssd_instance):
    def runner(*args):
        ssd_instance.execute_test(args)

    return runner


def run_cli_wo_flush(ssd_instance):
    def runner(*args):
        cli_args = [str(arg) for arg in args]
        full_command = f'{COMMAND_PREFIX} {cli_args[0]} {" ".join(cli_args[1:])}'
        subprocess.run(full_command, shell=True, check=True)

    return runner


@pytest.fixture
def ssd():
    ssd = SSD()
    ssd.initialize_ssd_nand()
    ssd.initialize_ssd_output()
    ssd._buffer.buffer_clear()
    return ssd


@pytest.fixture(params=['0', '50', '99'])
def valid_address(request):
    return request.param


@pytest.fixture(params=['100', '0220', '990', 'ABC'])
def invalid_address(request):
    return request.param


@pytest.fixture(params=['0x000000001', '0xFFFF', 'FFFFFF0', 'FFFFFF0000', '0xFXYZ0000'])
def invalid_value(request):
    return request.param


@pytest.fixture(params=['-1', '0', '11', '2000', 'A', 'None'])
def invalid_size(request):
    return request.param


def read_file_with_lines(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]


def read_buffer():
    ssd = SSD()
    return ssd._buffer._buffer_list
