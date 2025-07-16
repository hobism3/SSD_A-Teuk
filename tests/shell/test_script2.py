from pathlib import Path
from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell import Shell


@pytest.fixture
def case_list():
    ssd_path = Path(__file__).resolve().parents[2] / 'ssd.py'

    test_args_list = [
        ('W', '4', '0x00000000'),
        ('W', '0', '0x00000000'),
        ('W', '3', '0x00000000'),
        ('W', '1', '0x00000000'),
        ('W', '2', '0x00000000'),
        ('R', '4', None),
        ('R', '0', None),
        ('R', '3', None),
        ('R', '1', None),
        ('R', '2', None),
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


def test_shell_script2(capsys: pytest.CaptureFixture, mocker: MockerFixture, case_list):
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('builtins.input', side_effect=['2_', 'exit'])
    mocker.patch('builtins.open', mocker.mock_open(read_data='0x00000000'))
    mocker.patch('random.randint', return_value=0x00000000)
    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert '[2_PartialLBAWrite] PASS' in output

    for case in case_list:
        assert case in mock_run.call_args_list
