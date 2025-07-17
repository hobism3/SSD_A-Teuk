from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell import Shell
from shell_tool.shell_constants import RUN_SSD
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre

TEST_LBA = ['4', '0', '3', '1', '2']
TEST_ARGS_LIST = [('W', index, '0x00000000') for index in TEST_LBA] + [
    ('R', index, None) for index in TEST_LBA
]


@pytest.fixture
def case_list():
    test_cases = []
    for cmd, code, value in TEST_ARGS_LIST:
        cmd_args = RUN_SSD + [cmd, code]
        if value is not None:
            cmd_args.append(value)

        test_cases.append(call(cmd_args, check=True))

    return test_cases


def test_shell_script2(capsys: pytest.CaptureFixture, mocker: MockerFixture, case_list):
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('builtins.input', side_effect=['2_', 'exit'])
    mocker.patch('builtins.open', mocker.mock_open(read_data='0x00000000'))
    mocker.patch('random.randint', return_value=0x00000000)
    mocker.patch('commands.write.WriteCommand.parse_result', return_value=Msg.DONE)
    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert Pre.SCRIPT_2 + ' ' + Msg.PASS in output

    for case in case_list:
        assert case in mock_run.call_args_list
