from subprocess import CalledProcessError
from unittest.mock import patch

import pytest

from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from tests.shell.conftest import assert_command_called_once, run_shell_with_inputs
from tests.shell.constants import (
    SHELL_ERROR_TEST_CASES,
    SHELL_READ_THEN_EXIT,
    SHELL_SUBPROCESS_TEST_CASES,
    SHELL_TEST_CASES,
)


@pytest.mark.timeout(1)
@pytest.mark.parametrize('case', SHELL_TEST_CASES)
def test_shell_execution(
    shell, mock_commands, shell_user_inputs, shell_expected_called, case
):
    run_shell_with_inputs(shell, shell_user_inputs[case])
    assert_command_called_once(mock_commands, shell_expected_called[case])


@pytest.mark.timeout(1)
@pytest.mark.parametrize('case', SHELL_ERROR_TEST_CASES)
def test_shell_error_handling(shell, mock_subprocess_run, shell_user_inputs, case):
    with patch('builtins.input', side_effect=shell_user_inputs[case]):
        shell.run()
    mock_subprocess_run.assert_not_called()


@pytest.mark.timeout(1)
@pytest.mark.parametrize('case', SHELL_SUBPROCESS_TEST_CASES)
def test_subprocess_called(
    shell, mock_subprocess_run, shell_user_inputs, shell_expected_subprocess_cmd, case
):
    run_shell_with_inputs(shell, shell_user_inputs[case])
    mock_subprocess_run.assert_called_once_with(
        shell_expected_subprocess_cmd[case], check=True
    )


@pytest.mark.timeout(1)
def test_subprocess_error_logged(shell, mock_subprocess_run, shell_user_inputs, capsys):
    mock_subprocess_run.side_effect = CalledProcessError(1, ['dummy'])
    run_shell_with_inputs(shell, shell_user_inputs[SHELL_READ_THEN_EXIT])
    output = capsys.readouterr().out
    assert Msg.ERROR in output
    assert Pre.READ in output


def test_shell_run_serial_script_success(tmp_path, capsys):
    from shell import Shell

    script_path = tmp_path / 'script.txt'
    with open(script_path, 'w') as f:
        f.write('1_FullWriteAndReadCompare\n')

    shell = Shell()
    shell.run_serial_script(str(script_path))

    output = capsys.readouterr().out
    print(output)
    assert 'Run' in output
    assert 'Pass' in output


def test_shell_serial_script_file_not_found(capsys):
    from shell import Shell

    shell = Shell()
    shell.run_serial_script('nonexistent.txt')
    output = capsys.readouterr().out
    assert 'Script file not found' in output


@pytest.mark.skip
def test_shell_dot_task_runs_briefly(mocker, tmp_path, capsys):
    import time

    from shell import Shell

    mocker.patch(
        'commands.script1.FullWriteAndReadCompare.execute',
        side_effect=lambda x: time.sleep(1.5) or True,
    )
    script_path = tmp_path / 'script.txt'
    with open(script_path, 'w') as f:
        f.write('1_FullWriteAndReadCompare\n')

    shell = Shell()
    shell.run_serial_script(script_path)
    output = capsys.readouterr().out
    print(output)
    assert '.' in output
