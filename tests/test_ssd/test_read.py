from unittest.mock import patch

import pytest

from tests.test_ssd.conftest import (
    ERROR,
    INITIAL_VALUE,
    SSD_OUTPUT_FILE_PATH,
    VALID_VALUE,
    read_file_with_lines,
    run_direct,
)


@pytest.mark.parametrize('runner_factory', [run_direct])
@pytest.mark.parametrize('mock_return', [(False, '')])
@patch('ssd_tool.buffer.Buffer.read')
def test_ssd_read_initial_value_check(
    mock_read, mock_return, ssd, runner_factory, valid_address
):
    runner = runner_factory(ssd)
    mock_read.return_value = mock_return
    runner('R', valid_address)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [INITIAL_VALUE]


@pytest.mark.parametrize('runner_factory', [run_direct])
def test_ssd_read_fail_wrong_address(ssd, runner_factory, invalid_address):
    runner = runner_factory(ssd)
    runner('R', invalid_address)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


@pytest.mark.parametrize('runner_factory', [run_direct])
@pytest.mark.parametrize('mock_return', [(True, VALID_VALUE)])
@patch('ssd_tool.buffer.Buffer.read')
def test_ssd_read_written_value_pass(
    mock_read, mock_return, ssd, runner_factory, valid_address
):
    runner = runner_factory(ssd)
    mock_read.return_value = mock_return
    runner('R', valid_address)
    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [VALID_VALUE]
