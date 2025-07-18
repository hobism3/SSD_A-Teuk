from unittest.mock import patch

import pytest

from tests.test_ssd.conftest import (
    ERROR,
    SSD_OUTPUT_FILE_PATH,
    VALID_ADDRESS,
    VALID_VALUE,
    read_file_with_lines,
    run_direct,
)


@pytest.mark.parametrize('runner_factory', [run_direct])
@patch('ssd_tool.buffer.Buffer.buffer_arrange')
@patch('ssd_tool.buffer.Buffer.buffer_file_write')
def test_ssd_write_pass(
    mock_buffer_file_write, mock_buffer_arrange, ssd, runner_factory, valid_address
):
    runner = runner_factory(ssd)
    runner('W', valid_address, VALID_VALUE)
    assert mock_buffer_arrange.called

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value


@pytest.mark.parametrize('runner_factory', [run_direct])
@pytest.mark.parametrize(
    'address, value', [(None, VALID_VALUE), (VALID_ADDRESS, None), (None, None)]
)
def test_ssd_write_fail_not_enough_args(ssd, runner_factory, address, value):
    runner = runner_factory(ssd)
    runner('W', address, value)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


@pytest.mark.parametrize('runner_factory', [run_direct])
def test_ssd_write_fail_wrong_value(ssd, runner_factory, invalid_value):
    runner = runner_factory(ssd)
    runner('W', VALID_ADDRESS, invalid_value)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


@pytest.mark.parametrize('runner_factory', [run_direct])
def test_ssd_write_fail_wrong_address(ssd, runner_factory, invalid_address):
    runner = runner_factory(ssd)
    runner('W', invalid_address, VALID_VALUE)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]
