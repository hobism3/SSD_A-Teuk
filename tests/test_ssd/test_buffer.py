import pytest

from ssd_tool.buffer import Buffer
from tests.test_ssd.testcase.buffer_test_case import *


@pytest.fixture
def buffer():
    buffer = Buffer()
    buffer.buffer_clear()
    buffer._buffer_list = [['empty'], ['empty'], ['empty'], ['empty'], ['empty']]
    return buffer


def test_read_buffer_file(buffer):
    assert buffer.buffer_file_read() == [
        '1_empty',
        '2_empty',
        '3_empty',
        '4_empty',
        '5_empty',
    ]


def test_update_buffer_file(buffer):
    buffer._buffer_list = [
        ['E', 1, 1],
        ['E', 3, 1],
        ['E', 6, 1],
        ['E', 9, 1],
        ['E', 13, 1],
    ]
    buffer.buffer_file_write()
    assert buffer.buffer_file_read() == [
        '1_E_1_1',
        '2_E_3_1',
        '3_E_6_1',
        '4_E_9_1',
        '5_E_13_1',
    ]


@pytest.mark.parametrize(
    'input_data, expected',
    [(tc['input'], tc['expected']) for tc in buffer_arrange_test_case],
    ids=[tc['name'] for tc in buffer_arrange_test_case],
)
def test_buffer_arrange_with_mock(buffer, input_data, expected):
    for tc in input_data:
        buffer.buffer_arrange(tc[0], tc[1], tc[2], buffer.buffer_length)
    assert buffer._buffer_list == expected


@pytest.mark.parametrize(
    'input_data, expected',
    [(tc['input'], tc['expected']) for tc in buffer_read_test_case],
    ids=[tc['name'] for tc in buffer_read_test_case],
)
def test_buffer_read_with_mock(buffer, input_data, expected):
    buffer._buffer_list = input_data[0]
    assert buffer.read(input_data[1]) == expected


@pytest.mark.parametrize(
    'input_data, expected',
    [(tc['input'], tc['expected']) for tc in tc_test_buffer_is_full_with_mock],
)
def test_buffer_is_full_with_mock(buffer, input_data, expected):
    with pytest.raises(Exception):
        for tc in input_data:
            buffer.buffer_arrange(tc[0], tc[1], tc[2], buffer.buffer_length)
