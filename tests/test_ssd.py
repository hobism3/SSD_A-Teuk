import subprocess

from ssd import SSD


def test_ssd_initial_nand_value_check():
    with open('ssd_nand.txt') as f:
        actual_value_lines = f.readline()
    assert actual_value_lines[0] == '00 00000000'
    assert actual_value_lines[1] == '01 00000000'
    assert actual_value_lines[2] == '02 00000000'
    assert actual_value_lines[-1] == '99 00000000'


def test_ssd_read_initial_value_check():
    input_address = '00'
    expected_value = '00000000'
    ssd = SSD()

    ssd.read(input_address)
    with open('ssd_output.txt') as f:
        actual_value = f.readline()

    assert actual_value == expected_value
    input_address = '02'
    ssd.read(input_address)
    with open('ssd_output.txt') as f:
        actual_value = f.readline()

    assert actual_value == expected_value
    input_address = '99'
    ssd.read(input_address)
    with open('ssd_output.txt') as f:
        actual_value = f.readline()

    assert actual_value == expected_value


def test_ssd_write_pass():
    input_address = '00'
    input_value = '00000001'
    expected_value = ''
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value

    input_address = '02'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value

    input_address = '99'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value


def test_ssd_write_pass_check_value():
    input_address = '00'
    input_value = '00000001'
    expected_value = ''
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value

    with open('ssd_nand.txt') as f:
        actual_value = f.readline()
    assert actual_value[0] == '00 00000001'

    input_address = '02'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value

    with open('ssd_nand.txt') as f:
        actual_value = f.readline()
    assert actual_value[2] == '00 00000001'

    input_address = '99'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value
    with open('ssd_nand.txt') as f:
        actual_value = f.readline()
    assert actual_value[99] == '00 00000001'


def test_ssd_write_fail_wrong_address():
    input_address = '100'
    input_value = '00000001'
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value

    input_address = '0220'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value

    input_address = '0990'
    ssd.write(input_address, input_value)
    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value


def test_ssd_write_fail_no_value():
    input_address = '00'
    input_value = None
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value


def test_ssd_write_fail_no_address():
    input_address = None
    input_value = '00000001'
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value


def test_ssd_write_fail_no_both():
    input_address = None
    input_value = None
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value


def test_ssd_write_fail_wrong_value():
    input_address = '00'
    input_value = '000000010'
    expected_value = 'ERROR'
    ssd = SSD()
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value

    input_value = 'FFFFFF0'
    ssd.write(input_address, input_value)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value


def test_ssd_read_written_value_pass():
    input_address = '00'
    input_value = '00000001'
    ssd = SSD()

    ssd.write(input_address, input_value)
    ssd.read(input_address)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == input_value

    input_address = '02'
    ssd.write(input_address, input_value)
    ssd.read(input_address)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == input_value

    input_address = '99'
    ssd.write(input_address, input_value)
    ssd.read(input_address)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == input_value


def test_ssd_read_initial_value_w_command():
    command = 'python ssd.py R 0'
    expected_value = '00000000'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value

    command = 'python ssd.py R 2'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value

    command = 'python ssd.py R 99'
    subprocess.run(command)

    with open('ssd_output.txt') as f:
        actual_value = f.read()
    assert actual_value == expected_value
