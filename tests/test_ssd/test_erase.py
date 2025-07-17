import pytest

from tests.test_ssd.conftest import (
    ERROR,
    INITIAL_VALUE,
    SSD_NAND_FILE_PATH,
    SSD_OUTPUT_FILE_PATH,
    VALID_ADDRESS,
    VALID_SIZE,
    read_file_with_lines,
    run_cli,
    run_direct,
)


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_erase_pass(ssd, runner_factory, valid_address):
    runner = runner_factory(ssd)
    for valid_size in range(1, 10):
        if valid_address == '99':
            continue
        runner('E', valid_address, str(valid_size))
        actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
        assert not actual_value

        actual_value = read_file_with_lines(SSD_NAND_FILE_PATH)
        assert (
            actual_value[int(valid_address)]
            == f'{int(valid_address):02d} {INITIAL_VALUE}'
        )


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_erase_over_size(ssd, runner_factory, valid_address):
    runner = runner_factory(ssd)
    for valid_size in range(1, 10):
        if valid_address != '99':
            continue
        if valid_size == 1:
            runner('E', valid_address, str(valid_size))
            actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
            assert not actual_value

            actual_value = read_file_with_lines(SSD_NAND_FILE_PATH)
            assert (
                actual_value[int(valid_address)]
                == f'{int(valid_address):02d} {INITIAL_VALUE}'
            )
        else:
            runner('E', valid_address, str(valid_size))
            actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
            assert actual_value == [ERROR]


@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_erase_fail_not_invalid_size(ssd, runner_factory, invalid_size):
    runner = runner_factory(ssd)
    runner('E', VALID_ADDRESS, invalid_size)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]


@pytest.mark.parametrize(
    'address, size', [(None, VALID_SIZE), (VALID_ADDRESS, None), (None, None)]
)
@pytest.mark.parametrize('runner_factory', [run_direct, run_cli])
def test_ssd_erase_fail_not_enough_args(ssd, runner_factory, address, size):
    runner = runner_factory(ssd)
    runner('E', address, size)

    actual_value = read_file_with_lines(SSD_OUTPUT_FILE_PATH)
    assert actual_value == [ERROR]
