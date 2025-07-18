from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell import Shell
from shell_tool.shell_constants import RUN_SSD
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre


@pytest.fixture
def test_case_list(erase_case_list, write_case_list):
    return erase_case_list + write_case_list


@pytest.fixture
def erase_case_list():
    test_cases = []

    for index in range(2, 100, 2):
        size = '2' if index == 98 else '3'
        cmd_args = RUN_SSD + ['E', str(index), size]
        test_cases.append(call(cmd_args, check=True))

    return test_cases


@pytest.fixture
def write_case_list():
    test_cases = []

    for index in range(2, 100, 2):  # 2 ~ 98까지 짝수
        for _ in range(2):  # 같은 LBA 두 번
            cmd_args = RUN_SSD + ['W', str(index), '0x00000000']
            test_cases.append(call(cmd_args, check=True))

    return test_cases


@pytest.mark.skip
def test_shell_script4(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, test_case_list
):
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('builtins.input', side_effect=['4_', 'exit'])
    mocker.patch('random.randint', return_value=0x00000000)
    mocker.patch('commands.write.WriteCommand._parse_result', return_value=Msg.DONE)

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert Pre.SCRIPT_4 + ' ' + Msg.PASS in output

    for case in test_case_list:
        assert case in mock_run.call_args_list
