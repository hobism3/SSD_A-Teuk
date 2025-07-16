from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from shell import Shell

CASE_LIST = [
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'W',
            '04',
            '0x00000000',
        ],
        check=True,
    ),
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'W',
            '00',
            '0x00000000',
        ],
        check=True,
    ),
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'W',
            '03',
            '0x00000000',
        ],
        check=True,
    ),
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'W',
            '01',
            '0x00000000',
        ],
        check=True,
    ),
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'W',
            '02',
            '0x00000000',
        ],
        check=True,
    ),
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'R',
            '04',
        ],
        check=True,
    ),
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'R',
            '00',
        ],
        check=True,
    ),
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'R',
            '03',
        ],
        check=True,
    ),
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'R',
            '01',
        ],
        check=True,
    ),
    call(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'R',
            '02',
        ],
        check=True,
    ),
]


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
