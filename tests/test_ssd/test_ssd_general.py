import sys
from unittest.mock import MagicMock, patch

import pytest

from tests.test_ssd.conftest import (
    ERROR,
    INITIAL_VALUE,
    SSD_NAND_FILE_PATH,
    SSD_OUTPUT_FILE_PATH,
    VALID_ADDRESS,
    VALID_VALUE,
    read_buffer,
    read_file_with_lines,
    run_cli,
    run_cli_wo_flush,
    run_direct,
)


def test_ssd_initial_nand_value_check(ssd):
    actual_value_lines = read_file_with_lines(SSD_NAND_FILE_PATH)
    for idx, line in enumerate(actual_value_lines):
        assert line.strip() == f'{idx:02d} {INITIAL_VALUE}'


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_invalid_mode_w_command(ssd, runner_factory):
    runner = runner_factory(ssd)
    runner('M', VALID_ADDRESS, VALID_VALUE)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


@pytest.mark.parametrize('runner_factory', [run_cli_wo_flush])
def test_ssd_auto_flush_operation_with_cli(ssd, runner_factory):
    runner = runner_factory(ssd)
    for i in range(5):
        runner('W', str(i), VALID_VALUE)

    actual_value = read_file_with_lines(SSD_NAND_FILE_PATH)
    for i in range(5):
        assert actual_value[int(i)] == f'{int(i):02d} {INITIAL_VALUE}'

    runner('W', '0', str(int(VALID_VALUE, 16) + 0x00000001))

    actual_value = read_buffer()
    assert 'empty' not in actual_value

    actual_value = read_file_with_lines(SSD_NAND_FILE_PATH)
    for i in range(5):
        assert actual_value[int(i)] == f'{int(i):02d} {VALID_VALUE}'


@pytest.mark.parametrize('runner_factory', [run_cli])
@pytest.mark.parametrize('command', ['W', 'R', 'E', 'F'])
@patch('ssd.CommandFactory')
def test_ssd_read_initial_value_check(
    mock_command_factory, ssd, command, runner_factory
):
    mock_command = MagicMock()
    mock_command_factory.create_command.return_value = mock_command
    import ssd

    args = {
        'W': ['W', '2', '0x00000001'],
        'R': ['R', '2'],
        'E': ['E', '2', '2'],
        'F': ['F'],
    }
    sys.argv = args[command]
    ssd.main()
    mock_command.execute.assert_called_once()
