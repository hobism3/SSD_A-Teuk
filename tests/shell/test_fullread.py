import pytest
from pytest_mock import MockerFixture

from shell import Shell


def test_shell_fullread(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('builtins.input', side_effect=['fullread', 'exit'])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Full Read]' in output
    mock_run.assert_called_with(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'R',
            '99',
        ],
        check=True,
    )


def test_shell_fullread_exception(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    mocker.patch('builtins.input', side_effect=['fullread 0 0 0', 'exit'])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Read]  ERROR' in output
