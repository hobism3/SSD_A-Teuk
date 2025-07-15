import os
import subprocess

import pytest

from ssd import SSD, SSD_NAND_FILE_PATH, SSD_OUTPUT_FILE_PATH

COMMAND_WRITE = 'python ../ssd.py W'
COMMAND_READ = 'python ../ssd.py R'
COMMAND_INVALID = 'python ../ssd.py M'

ERROR = 'ERROR'

VALID_ADDRESS = '00'
INVALID_ADDRESS = '100'
INITIAL_VALUE = '0x00000000'
VALID_VALUE = '0x00000001'


@pytest.fixture
def ssd():
    ssd = SSD()
    ssd.initialize_ssd_nand()
    ssd.initialize_ssd_output()
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


def read_file_with_lines(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]


def test_ssd_initial_nand_value_check(ssd):
    actual_value_lines = read_file_with_lines(SSD_NAND_FILE_PATH)
    for idx, line in enumerate(actual_value_lines):
        assert line.strip() == f'{idx:02d} {INITIAL_VALUE}'


def test_ssd_write_pass(ssd, valid_address):
    ssd.execute('W', valid_address, VALID_VALUE)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value


def test_ssd_write_pass_check_value(ssd, valid_address):
    ssd.execute('W', valid_address, VALID_VALUE)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value

    actual_value = read_file_with_lines(SSD_NAND_FILE_PATH)
    assert actual_value[int(valid_address)] == f'{int(valid_address):02d} {VALID_VALUE}'


def test_ssd_write_fail_wrong_address(ssd, invalid_address):
    ssd.execute('W', invalid_address, VALID_VALUE)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_fail_no_value(ssd):
    ssd.execute('W', VALID_ADDRESS, None)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_fail_no_address(ssd):
    ssd.execute('W', None, VALID_VALUE)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_fail_no_both(ssd):
    ssd.execute('W', None, None)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_fail_wrong_value(ssd, invalid_value):
    ssd.execute('W', VALID_ADDRESS, invalid_value)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]

def test_ssd_invalid_mode_w_command(ssd):
    subprocess.run(f'{COMMAND_INVALID} {VALID_ADDRESS} {VALID_VALUE}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]

def test_ssd_write_pass_w_command(ssd):
    subprocess.run(f'{COMMAND_WRITE} {VALID_ADDRESS} {VALID_VALUE}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value


def test_ssd_write_fail_w_command_wrong_address(ssd, invalid_address):
    subprocess.run(f'{COMMAND_WRITE} {invalid_address} {VALID_VALUE}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_fail_w_command_wrong_value(ssd, invalid_value):
    subprocess.run(f'{COMMAND_WRITE} {VALID_ADDRESS} {invalid_value}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_fail_w_command_no_value(ssd):
    subprocess.run(f'{COMMAND_WRITE} {VALID_ADDRESS}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_fail_w_command_no_address(ssd):
    subprocess.run(f'{COMMAND_WRITE} {VALID_VALUE}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_fail_w_command_no_both(ssd):
    subprocess.run(f'{COMMAND_WRITE}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_read_initial_value_check(ssd, valid_address):
    ssd.execute('R', valid_address)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [INITIAL_VALUE]


def test_ssd_read_written_value_pass(ssd, valid_address):
    ssd.execute('W', valid_address, VALID_VALUE)
    ssd.execute('R', valid_address)
    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)

    assert actual_value == [VALID_VALUE]


def test_ssd_read_fail_wrong_address(ssd, invalid_address):
    ssd.execute('R', invalid_address)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_read_initial_value_w_command(ssd, valid_address):
    command = f'{COMMAND_READ} {valid_address}'
    subprocess.run(command)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [INITIAL_VALUE]


def test_ssd_read_write_pass_w_command(ssd, valid_address):
    command = f'{COMMAND_WRITE} {valid_address} {VALID_VALUE}'
    subprocess.run(command)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value

    command = f'{COMMAND_READ} {valid_address}'
    subprocess.run(command)
    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [VALID_VALUE]
