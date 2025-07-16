from _pytest.capture import CaptureFixture
import pytest

from tests.shell.conftest import run_command_with_args
from tests.shell.constants import (
    CMD_INVALID_TEST_CASES,
    CMD_TEST_CASES,
)


@pytest.mark.timeout(1)
@pytest.mark.parametrize('case', CMD_TEST_CASES)
def test_command_execution(
    capsys: CaptureFixture, case, cmd_input_args, cmd_expected_msg
):
    run_command_with_args(*cmd_input_args[case])
    captured = capsys.readouterr()
    output = captured.out
    assert cmd_expected_msg[case] in output


@pytest.mark.timeout(1)
@pytest.mark.parametrize('case', CMD_INVALID_TEST_CASES)
def test_command_invalid_execution(
    capsys: CaptureFixture, case, cmd_input_args, cmd_expected_msg
):
    run_command_with_args(*cmd_input_args[case])
    captured = capsys.readouterr()
    assert cmd_expected_msg[case] in captured.out
