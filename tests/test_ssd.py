import subprocess

import pytest

from ssd import SSD


def test_ssd_initial_nand_value_check():
    ssd = SSD()
    ssd.read('00')
    with open('ssd_nand.txt') as f:
        actual_value_lines = f.readlines()
    assert actual_value_lines[0].strip() == '00 0x00000000'
    assert actual_value_lines[1].strip() == '01 0x00000000'
    assert actual_value_lines[2].strip() == '02 0x00000000'
    assert actual_value_lines[-1].strip() == '99 0x00000000'


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


def test_ssd_write_pass():
    input_address = '00'
    input_value = '0x00000001'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()
    assert not actual_value

    input_address = '02'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()
    assert not actual_value

    input_address = '99'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()
    assert not actual_value


def test_ssd_write_pass_check_value():
    input_address = '00'
    input_value = '0x00000001'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.readlines()
    assert not actual_value

    with open('ssd_nand.txt') as f:
        actual_value = f.readlines()
    assert actual_value[0].strip() == '00 0x00000001'

    input_address = '02'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()
    assert not actual_value

    with open('ssd_nand.txt') as f:
        actual_value = f.readlines()
    assert actual_value[2].strip() == '02 0x00000001'

    input_address = '99'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.readlines()
    assert not actual_value

    with open('ssd_nand.txt') as f:
        actual_value = f.readlines()
    assert actual_value[99].strip() == '99 0x00000001'


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
