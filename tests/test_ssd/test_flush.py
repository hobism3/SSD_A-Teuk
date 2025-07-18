from unittest.mock import patch

import pytest

from tests.test_ssd.conftest import (
    run_direct_wo_flush,
)


@pytest.mark.parametrize('runner_factory', [run_direct_wo_flush])
@pytest.mark.parametrize(
    'mock_return',
    [
        [['empty'], ['empty'], ['empty'], ['empty'], ['empty']],
        [['E', 3, 3], ['E', 9, 3], ['empty'], ['empty'], ['empty']],
        [['W', 2, '0x00000001'], ['empty'], ['empty'], ['empty'], ['empty']],
    ],
)
@patch('ssd_tool.buffer.Buffer.buffer_file_read_as_list')
def test_ssd_flush_pass(
    mock_buffer_file_read_as_list, mock_return, ssd, runner_factory
):
    runner = runner_factory(ssd)
    mock_buffer_file_read_as_list.return_value = mock_return
    runner('F')
    with (
        patch.object(ssd, '_write', autospec=True) as mock_write,
        patch.object(ssd, '_erase', autospec=True) as mock_erase,
        patch.object(ssd._buffer, 'buffer_clear', autospec=True) as mock_clear,
    ):
        runner('F')

        assert mock_write.call_count == sum(1 for b in mock_return if b[0] == 'W')
        assert mock_erase.call_count == sum(1 for b in mock_return if b[0] == 'E')
        mock_clear.assert_called_once()


@pytest.mark.parametrize('runner_factory', [run_direct_wo_flush])
@pytest.mark.parametrize(
    'mock_return',
    [
        [['E', 1, 1], ['E', 3, 1], ['E', 5, 1], ['E', 7, 1], ['E', 9, 1]],
        [['E', 1, 1], ['E', 3, 1], ['E', 5, 1], ['E', 7, 1], ['empty']],
    ],
)
@patch('ssd_tool.buffer.Buffer.buffer_file_read_as_list')
def test_ssd_auto_flush_operation_with_direct(
    mock_buffer_file_read_as_list, mock_return, ssd, runner_factory
):
    runner = runner_factory(ssd)
    mock_buffer_file_read_as_list.return_value = mock_return
    with patch.object(ssd, 'flush', autospec=True) as mock_flush:
        runner('R', '0')
        if ssd._buffer.buffer_length == 5:
            mock_flush.assert_called_once()
        else:
            mock_flush.assert_not_called()
