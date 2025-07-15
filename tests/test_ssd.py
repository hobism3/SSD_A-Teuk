import os
import subprocess

import pytest

from ssd import SSD, SSD_NAND_FILE_PATH, SSD_OUTPUT_FILE_PATH

COMMAND_WRITE = 'python ../ssd.py W'
COMMAND_READ = 'python ../ssd.py R'

ERROR = 'ERROR'

VALID_ADDRESS = '00'
INVALID_ADDRESS = '100'
INITIAL_VALUE = '0x00000000'
VALID_VALUE = '0x00000001'


@pytest.fixture
def ssd():
    ssd = SSD()
    ssd.initialize_ssd_nand()
    return ssd


@pytest.fixture(
    params=[('0', INITIAL_VALUE), ('50', INITIAL_VALUE), ('99', INITIAL_VALUE)]
)
def sample_input_address_w_initial_value(request):
    return request.param


@pytest.fixture(params=[('0', VALID_VALUE), ('50', VALID_VALUE), ('99', VALID_VALUE)])
def sample_input_address(request):
    return request.param


@pytest.fixture(
    params=[('100', VALID_VALUE), ('0220', VALID_VALUE), ('990', VALID_VALUE)]
)
def sample_input_address_wrong(request):
    return request.param


@pytest.fixture(
    params=[
        (VALID_ADDRESS, '0x000000001'),
        (VALID_ADDRESS, '0xFFFF'),
        (VALID_ADDRESS, 'FFFFFF0'),
    ]
)
def sample_input_value_wrong(request):
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


def test_ssd_write_pass(ssd, sample_input_address):
    input_address, input_value = sample_input_address
    ssd.execute('W', input_address, input_value)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value


def test_ssd_write_pas_scheck_value(ssd, sample_input_address):
    input_address, input_value = sample_input_address
    ssd.execute('W', input_address, input_value)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value

    actual_value = read_file_with_lines(SSD_NAND_FILE_PATH)
    assert actual_value[int(input_address)] == f'{int(input_address):02d} {input_value}'


def test_ssd_write_fail_wrong_address(ssd, sample_input_address_wrong):
    input_address, input_value = sample_input_address_wrong
    ssd.execute('W', input_address, input_value)

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


def test_ssd_write_fail_wrong_value(ssd, sample_input_value_wrong):
    input_address, input_value = sample_input_value_wrong
    ssd.execute('W', input_address, input_value)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_pass_w_command(ssd):
    subprocess.run(f'{COMMAND_WRITE} {VALID_ADDRESS} {VALID_VALUE}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value


def test_ssd_write_fail_w_command_wrong_address(ssd, sample_input_address_wrong):
    input_address, input_value = sample_input_address_wrong
    subprocess.run(f'{COMMAND_WRITE} {input_address} {input_value}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_write_fail_w_command_wrong_value(ssd, sample_input_value_wrong):
    input_address, input_value = sample_input_value_wrong
    subprocess.run(f'{COMMAND_WRITE} {input_address} {input_value}')

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


def test_ssd_read_initial_value_check(ssd, sample_input_address_w_initial_value):
    input_address, expected_value = sample_input_address_w_initial_value
    ssd.execute('R', input_address)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [expected_value]


def test_ssd_read_written_value_pass(ssd, sample_input_address):
    input_address, input_value = sample_input_address

    ssd.execute('W', input_address, input_value)
    ssd.execute('R', input_address)
    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)

    assert actual_value == [input_value]


def test_ssd_read_fail_wrong_address(ssd, sample_input_address_wrong):
    ssd.execute('R', sample_input_address_wrong[0])

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


def test_ssd_read_initial_value_w_command(ssd, sample_input_address_w_initial_value):
    input_address, expected_value = sample_input_address_w_initial_value
    command = f'{COMMAND_READ} {input_address}'
    subprocess.run(command)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [expected_value]


def test_ssd_read_write_pass_w_command(ssd, sample_input_address):
    input_address, input_value = sample_input_address
    command = f'{COMMAND_WRITE} {input_address} {input_value}'
    subprocess.run(command)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value

    command = f'{COMMAND_READ} {input_address}'
    subprocess.run(command)
    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [input_value]
