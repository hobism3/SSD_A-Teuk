import os
import subprocess

import pytest

from ssd import SSD, SSD_NAND_FILE_PATH, SSD_OUTPUT_FILE_PATH

COMMAND_PREFIX = 'python ../ssd.py'

ERROR = 'ERROR'

VALID_ADDRESS = '00'
INVALID_ADDRESS = '100'
INITIAL_VALUE = '0x00000000'
VALID_VALUE = '0x00000001'


def run_direct(ssd_instance):
    def runner(command, *args):
        ssd_instance.execute(command, *args)

    return runner


def run_cli(ssd_instance):
    def runner(command, *args):
        cli_args = [str(arg) for arg in args]
        full_command = f'{COMMAND_PREFIX} {command} {" ".join(cli_args)}'
        subprocess.run(full_command, shell=True, check=True)

    return runner


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


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_write_pass(ssd, runner_factory, valid_address):
    runner = runner_factory(ssd)
    runner('W', valid_address, VALID_VALUE)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value

    actual_value = read_file_with_lines(SSD_NAND_FILE_PATH)
    assert actual_value[int(valid_address)] == f'{int(valid_address):02d} {VALID_VALUE}'


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
@pytest.mark.parametrize(
    'address, value', [(None, VALID_VALUE), (VALID_ADDRESS, None), (None, None)]
)
def test_ssd_write_fail_not_enough_args(ssd, runner_factory, address, value):
    runner = runner_factory(ssd)
    runner('W', address, value)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]

def test_ssd_invalid_mode_w_command(ssd):
    subprocess.run(f'{COMMAND_INVALID} {VALID_ADDRESS} {VALID_VALUE}')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]

@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_write_fail_wrong_value(ssd, runner_factory, invalid_value):
    runner = runner_factory(ssd)
    runner('W', VALID_ADDRESS, invalid_value)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_write_fail_wrong_address(ssd, runner_factory, invalid_address):
    runner = runner_factory(ssd)
    runner('W', invalid_address, VALID_VALUE)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_read_initial_value_check(ssd, runner_factory, valid_address):
    runner = runner_factory(ssd)
    runner('R', valid_address)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [INITIAL_VALUE]


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_read_fail_wrong_address(ssd, runner_factory, invalid_address):
    runner = runner_factory(ssd)
    runner('R', invalid_address)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_read_written_value_pass(ssd, runner_factory, valid_address):
    runner = runner_factory(ssd)

    runner('W', valid_address, VALID_VALUE)
    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value

    runner('R', valid_address)
    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [VALID_VALUE]
