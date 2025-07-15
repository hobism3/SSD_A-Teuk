import os
import subprocess

import pytest

from ssd import SSD, SSD_NAND_FILE_PATH, SSD_OUTPUT_FILE_PATH

INITIAL_VALUE = '0x00000000'
VALID_VALUE = '0x00000001'


@pytest.fixture
def ssd():
    return SSD()


@pytest.fixture(params=[('0', VALID_VALUE), ('50', VALID_VALUE), ('99', VALID_VALUE)])
def sample_input_address(request):
    return request.param


def read_file(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]


def test_ssd_initial_nand_value_check(ssd):
    actual_value_lines = read_file(SSD_OUTPUT_FILE_PATH)
    for idx, line in enumerate(actual_value_lines):
        assert line.strip() == f'{idx:02d} {INITIAL_VALUE}'


def test_ssd_write_pass(ssd, sample_input_address):
    input_address, input_value = sample_input_address
    ssd.write(input_address, input_value)

    actual_value = read_file(SSD_OUTPUT_FILE_PATH)
    assert not actual_value


def test_ssd_write_pass_check_value(ssd, sample_input_address):
    input_address, input_value = sample_input_address
    ssd.write(input_address, input_value)

    actual_value = read_file(SSD_OUTPUT_FILE_PATH)
    assert not actual_value

    actual_value = read_file(SSD_NAND_FILE_PATH)
    assert actual_value[int(input_address)] == f'{int(input_address):02d} {input_value}'


def test_ssd_write_fail_wrong_address():
    input_address = '100'
    input_value = '0x00000001'
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    input_address = '0220'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    input_address = '0990'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value


def test_ssd_write_fail_no_value():
    input_address = '00'
    input_value = None
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value


def test_ssd_write_fail_no_address():
    input_address = None
    input_value = '0x00000001'
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value


def test_ssd_write_fail_no_both():
    input_address = None
    input_value = None
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value


def test_ssd_write_fail_wrong_value():
    input_address = '00'
    input_value = '0x000000010'
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    input_value = 'FFFFFF0'
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value


@pytest.mark.skip
def test_ssd_read_initial_value_check():
    input_address = '00'
    expected_value = '0x00000000'
    ssd = SSD()

    ssd.read(input_address)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()

    assert actual_value == expected_value
    input_address = '02'
    ssd.read(input_address)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()

    assert actual_value == expected_value
    input_address = '99'
    ssd.read(input_address)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()

    assert actual_value == expected_value


@pytest.mark.skip
def test_ssd_read_written_value_pass():
    input_address = '00'
    input_value = '0x00000001'
    ssd = SSD()

    ssd.write(input_address, input_value)
    ssd.read(input_address)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == input_value

    input_address = '02'
    ssd.write(input_address, input_value)
    ssd.read(input_address)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == input_value

    input_address = '99'
    ssd.write(input_address, input_value)
    ssd.read(input_address)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == input_value


@pytest.mark.skip
def test_ssd_read_initial_value_w_command():
    command = 'python ssd.py R 0'
    expected_value = '0x00000000'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    command = 'python ssd.py R 2'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    command = 'python ssd.py R 99'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value


@pytest.mark.skip
def test_ssd_read_fail_wrong_address():
    input_address = '100'
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.read(input_address)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value


def test_ssd_write_pass_w_command():
    command = 'python ../ssd.py W 0 0x00000001'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()
    assert not actual_value


@pytest.mark.skip
def test_ssd_read_write_pass_w_command():
    command = 'python ssd.py W 0 0x00000001'
    subprocess.run(command)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()
    assert not actual_value

    command = 'python ssd.py R 0'
    subprocess.run(command)
    expected_value = '0x00000001'
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()
    assert actual_value == expected_value


def test_ssd_write_fail_w_command():
    command = 'python ../ssd.py W 100 0x00000001'
    expected_value = 'ERROR'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    command = 'python ../ssd.py W 02 0x0000001'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    command = 'python ../ssd.py W 099 0x000000001'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    command = 'python ../ssd.py W 0x00000001'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    command = 'python ../ssd.py W 00'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value

    command = 'python ../ssd.py W'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()[0].strip()
    assert actual_value == expected_value
