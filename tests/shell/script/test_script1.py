from pathlib import Path
from unittest.mock import call, mock_open

import pytest
from pytest_mock import MockerFixture

from shell import Shell
from shell_constants import MAX_LBA, SCRIPT_1_STEP
from shell_constants import ShellMsg as Msg


@pytest.fixture
def case_list():
    ssd_path = Path(__file__).resolve().parents[3] / 'ssd.py'

    test_args_list = [('W', str(i), '0xAAAABBBB') for i in range(100)] + [
        ('R', str(i), None) for i in range(100)
    ]

    test_cases = []
    for cmd, code, value in test_args_list:
        cmd_args = [
            'python',
            str(ssd_path),
            cmd,
            code,
        ]
        if value is not None:
            cmd_args.append(value)

        test_cases.append(call(cmd_args, check=True))

    return test_cases


def test_script1_call_subprocess_and_file_with_fullname(mocker):
    mock_run = mocker.patch('commands.base.subprocess.run')
    mock_open_file = mocker.patch('builtins.open', mock_open(read_data=''))
    mocker.patch('builtins.input', side_effect=['1_FullWriteAndReadCompare', 'exit'])
    mocker.patch('commands.read.ReadCommand.execute', return_value='0xAAAABBBB')

    shell = Shell()
    shell.run()

    assert mock_run.called
    assert mock_open_file.called


def test_script1_call_subprocess_and_file_with_shortname(mocker):
    mock_run = mocker.patch('commands.base.subprocess.run')
    mock_open_file = mocker.patch('builtins.open', mock_open(read_data=''))
    mocker.patch('builtins.input', side_effect=['1_', 'exit'])
    mocker.patch('commands.read.ReadCommand.execute', return_value='0xAAAABBBB')

    shell = Shell()
    shell.run()

    assert mock_run.called
    assert mock_open_file.called


def test_script1_pass_with_no_include_any_error(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, case_list
):
    mock_process = mocker.Mock()
    mock_process.returncode = 0
    mocker.patch('builtins.input', side_effect=['1_', 'exit'])
    mocker.patch('builtins.open', mocker.mock_open(read_data='0xAAAABBBB'))
    mocker.patch('commands.write.WriteCommand.parse_result', return_value=Msg.DONE)
    mocker.patch(
        'commands.script1.FullWriteAndReadCompare._generate_random_value_lst',
        return_value=[
            '0xAAAABBBB' for _ in range(MAX_LBA + SCRIPT_1_STEP // SCRIPT_1_STEP)
        ],
    )

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert '[1_FullWriteAndReadCompare] PASS' in output
    assert 'ERROR' not in output


def test_script1_valid_call_args_list(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, case_list
):
    mock_process = mocker.Mock()
    mock_process.returncode = 0
    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('builtins.input', side_effect=['1_', 'exit'])
    mocker.patch('builtins.open', mocker.mock_open(read_data='0xAAAABBBB'))
    mocker.patch('commands.write.WriteCommand.parse_result', return_value=Msg.DONE)
    mocker.patch(
        'commands.script1.FullWriteAndReadCompare._generate_random_value_lst',
        return_value=[
            '0xAAAABBBB' for _ in range(MAX_LBA + SCRIPT_1_STEP // SCRIPT_1_STEP)
        ],
    )

    shell = Shell()
    shell.run()

    for case in case_list:
        assert case in mock_run.call_args_list
