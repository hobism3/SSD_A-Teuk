import pytest

from tests.test_ssd.conftest import (
    ERROR,
    SSD_NAND_FILE_PATH,
    SSD_OUTPUT_FILE_PATH,
    VALID_ADDRESS,
    VALID_VALUE,
    read_file_with_lines,
    run_cli,
    run_direct,
)


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
