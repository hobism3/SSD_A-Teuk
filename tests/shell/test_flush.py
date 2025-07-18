from subprocess import CalledProcessError

import pytest
from pytest_mock import MockerFixture

from shell import Shell
from shell_tool.shell_constants import RUN_SSD
from shell_tool.shell_constants import ShellMsg
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre


def test_shell_read(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('builtins.input', side_effect=['flush', 'exit'])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert Pre.FLUSH + ' ' + Msg.DONE in output
    mock_run.assert_called_with(
        RUN_SSD + ['F'],
        check=True,
    )


def test_shell_read_exception_called_process_error(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    mocker.patch('builtins.input', side_effect=['flush', 'exit'])
    mocker.patch(
        'subprocess.run',
        side_effect=CalledProcessError(returncode=1, cmd='dummy command'),
    )

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert Pre.FLUSH + ' ' + Msg.ERROR in output


def test_shell_read_exception_value_error(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    mocker.patch('builtins.input', side_effect=['flush 0 0', 'exit'])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert ShellMsg.FLUSH_HELP in output
