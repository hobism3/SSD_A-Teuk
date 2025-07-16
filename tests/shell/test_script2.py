from pathlib import Path
from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell import Shell


@pytest.fixture
def case_list():
    ssd_path = Path(__file__).resolve().parents[2] / 'ssd.py'

    test_args_list = [
        ('W', '04', '0x00000000'),
        ('W', '00', '0x00000000'),
        ('W', '03', '0x00000000'),
        ('W', '01', '0x00000000'),
        ('W', '02', '0x00000000'),
        ('R', '04', None),
        ('R', '00', None),
        ('R', '03', None),
        ('R', '01', None),
        ('R', '02', None),
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
    assert '[2_PartialLBAWrite] Pass' in output

    for case in case_list:
        assert case in mock_run.call_args_list
