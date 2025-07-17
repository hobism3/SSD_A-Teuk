from unittest.mock import patch

import pytest

from tests.test_ssd.conftest import (
    INITIAL_VALUE,
    SSD_NAND_FILE_PATH,
    SSD_OUTPUT_FILE_PATH,
    VALID_VALUE,
    read_buffer,
    read_file_with_lines,
    run_cli_wo_flush,
    run_direct_wo_flush,
)


@pytest.mark.parametrize('runner_factory', [run_direct_wo_flush, run_cli_wo_flush])
def test_ssd_flush_pass(ssd, runner_factory):
    runner = runner_factory(ssd)
    runner('F')

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert not actual_value

    actual_value = read_buffer()
    assert 'empty' not in actual_value


@pytest.mark.parametrize('runner_factory', [run_direct_wo_flush])
def test_ssd_auto_flush_operation_with_direct(ssd, runner_factory):
    runner = runner_factory(ssd)
    with patch('ssd.SSD.flush') as mock_flush:
        for i in range(5):
            runner('W', str(i), VALID_VALUE)

        mock_flush.assert_not_called()
        runner('R', '0')
        mock_flush.assert_called_once()

        mock_flush.reset_mock()
        actual_value = read_buffer()
        assert 'empty' not in actual_value


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
