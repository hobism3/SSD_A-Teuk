from pathlib import Path
from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell import Shell

SSD_PATH = Path(__file__).resolve().parents[2] / 'ssd.py'

TEST_ARGS_LIST = [
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


CASE_LIST = []
for cmd, code, value in TEST_ARGS_LIST:
    cmd_args = [
        'python',
        str(SSD_PATH),
        cmd,
        code,
    ]
    if value is not None:
        cmd_args.append(value)

    CASE_LIST.append(call(cmd_args, check=True))


def test_shell_script2(capsys: pytest.CaptureFixture, mocker: MockerFixture):
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

    for case in CASE_LIST:
        assert case in mock_run.call_args_list
