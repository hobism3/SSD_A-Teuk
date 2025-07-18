from unittest.mock import call, mock_open

import pytest
from pytest_mock import MockerFixture

from shell import Shell
from shell_tool.shell_constants import RUN_SSD
from shell_tool.shell_constants import ShellMsg as Msg


@pytest.fixture
def mock_run(mocker):
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    # subprocess.run을 포함한 patch 설정
    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('random.getrandbits', return_value=0xAAAABBBB)
    mocker.patch('builtins.open', mocker.mock_open(read_data='0xAAAABBBB'))
    mocker.patch('commands.write.WriteCommand._parse_result', return_value=Msg.DONE)
    mocker.patch('commands.script3.range', return_value=range(1))

    return mock_run


@pytest.fixture
def case_list():
    test_args_list = [
        ('W', '0', '0xAAAABBBB'),
        ('W', '99', '0xAAAABBBB'),
        ('R', '0', None),
        ('R', '99', None),
    ]

    test_cases = []
    for cmd, code, value in test_args_list:
        cmd_args = RUN_SSD + [cmd, code]
        if value is not None:
            cmd_args.append(value)

        test_cases.append(call(cmd_args, check=True))

    return test_cases


def test_script3_call_subprocess_and_file_with_fullname(
    mocker: MockerFixture, mock_run
):
    mock_open_file = mocker.patch('builtins.open', mock_open(read_data=''))
    mocker.patch('builtins.input', side_effect=['3_WriteReadAging', 'exit'])

    shell = Shell()
    shell.run()

    assert mock_run.called
    assert mock_open_file.called


def test_script3_call_subprocess_and_file_with_shortname(mocker, mock_run):
    mock_open_file = mocker.patch('builtins.open', mock_open(read_data=''))
    mocker.patch('builtins.input', side_effect=['3_', 'exit'])

    shell = Shell()
    shell.run()

    assert mock_run.called
    assert mock_open_file.called


def test_script3_pass_with_no_include_any_error(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.input', side_effect=['3_', 'exit'])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert '[3_WriteReadAging] PASS' in output
    assert 'ERROR' not in output


def test_script3_valid_call_args_list(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, case_list, mock_run
):
    mocker.patch('builtins.input', side_effect=['3_', 'exit'])

    shell = Shell()
    shell.run()

    for case in case_list:
        assert case in mock_run.call_args_list


def test_script3_call_args_order(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, case_list, mock_run
):
    mocker.patch('builtins.input', side_effect=['3_', 'exit'])

    shell = Shell()
    shell.run()

    mock_run.assert_has_calls(case_list, any_order=False)
