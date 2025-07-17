import pytest

from tests.test_ssd.conftest import (
    ERROR,
    INITIAL_VALUE,
    SSD_NAND_FILE_PATH,
    SSD_OUTPUT_FILE_PATH,
    VALID_ADDRESS,
    VALID_VALUE,
    read_file_with_lines,
    run_cli,
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
