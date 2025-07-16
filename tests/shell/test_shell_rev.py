from subprocess import CalledProcessError
from unittest.mock import patch

from _pytest.capture import CaptureFixture
import pytest

from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre
from tests.shell.conftest import assert_command_called_once, run_shell_with_inputs


@pytest.mark.timeout(1)
@pytest.mark.parametrize(
    'case',
    [
        'help_exit',
        'just_exit',
        'write_then_exit',
        'read_then_exit',
        'empty_and_exit',
        'unknown_then_exit',
        'whitespace_and_case',
        'exit_mid_loop',
    ],
)
def test_shell_execution(shell, mock_commands, user_inputs, expected_called, case):
    run_shell_with_inputs(shell, user_inputs[case])
    assert_command_called_once(mock_commands, expected_called[case])


@pytest.mark.timeout(1)
@pytest.mark.parametrize('case', ['keyboard_interrupt', 'eof'])
def test_shell_error(shell, mock_subprocess_run, user_inputs, case):
    with patch('builtins.input', side_effect=user_inputs[case]):
        shell.run()
    mock_subprocess_run.assert_not_called()


@pytest.mark.timeout(1)
@pytest.mark.parametrize(
    'case', ['write_then_exit', 'read_then_exit', 'whitespace_and_case']
)
def test_subprocess_called(
    shell, mock_subprocess_run, user_inputs, case, expected_subprocess_cmd
):
    run_shell_with_inputs(shell, user_inputs[case])
    mock_subprocess_run.assert_called_once_with(
        expected_subprocess_cmd[case], check=True
    )


@pytest.mark.timeout(1)
def test_subprocess_error_logged(
    shell, mock_subprocess_run, user_inputs, capsys: CaptureFixture
):
    mock_subprocess_run.side_effect = CalledProcessError(1, ['dummy'])
    run_shell_with_inputs(shell, user_inputs['read_then_exit'])
    output = capsys.readouterr().out
    assert Msg.ERROR in output
    assert Pre.READ in output
