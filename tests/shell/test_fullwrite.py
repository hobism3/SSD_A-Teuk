import pytest
from pytest_mock import MockerFixture

from shell import Shell


def test_shell_fullwrite(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('builtins.input', side_effect=['fullwrite 0xFFFFFFFF', 'exit'])

    shell = Shell(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Full Write] Done' in output
    mock_run.assert_called_with(
        [
            'python',
            'C:\\Users\\User\\PycharmProjects\\pythonProject31\\ssd.py',
            'W',
            '99',
            '0xFFFFFFFF',
        ],
        check=True,
    )


def test_shell_fullwrite_invalid_input(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    ssd = mocker.Mock()

    mocker.patch('builtins.input', side_effect=['fullwrite 0 0', 'exit'])

    shell = Shell(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Read]  ERROR' in output
