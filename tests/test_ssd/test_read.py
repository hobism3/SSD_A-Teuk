import pytest

from tests.test_ssd.conftest import (
    ERROR,
    INITIAL_VALUE,
    SSD_OUTPUT_FILE_PATH,
    VALID_VALUE,
    read_file_with_lines,
    run_cli,
    run_direct,
)


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
