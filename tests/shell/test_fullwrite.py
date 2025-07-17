from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell import Shell
from shell_tool.shell_constants import LBA_RANGE, RUN_SSD
from shell_tool.shell_constants import ShellCmd as Cmd
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre

TEST_DATA = '0xFFFFFFFF'


@pytest.fixture
def case_list():
    test_cases = []
    for index in LBA_RANGE:
        cmd_args = RUN_SSD + [
            'W',
            str(index),
            TEST_DATA,
        ]
        test_cases.append(call(cmd_args, check=True))

    return test_cases


def test_shell_fullwrite(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, case_list
):
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch(
        'builtins.input', side_effect=[f'{Cmd.FULLWRITE} {TEST_DATA}', Cmd.EXIT]
    )

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert Pre.FULLWRITE + ' ' + Msg.DONE in output
    for case in case_list:
        assert case in mock_run.call_args_list


def test_shell_fullwrite_invalid_input(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    mocker.patch('builtins.input', side_effect=['fullwrite 0 0', 'exit'])
    mocker.patch('commands.write.WriteCommand.execute', side_effect=ValueError)

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert Pre.FULLWRITE + ' ' + Msg.ERROR in output
