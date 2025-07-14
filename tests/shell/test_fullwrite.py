import pytest
from pytest_mock import MockerFixture

from shell import Shell


def test_shell_fullwrite(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()

    mocker.patch('builtins.input', side_effect=['fullwrite 0xFFFFFFFF', 'exit'])

    shell = Shell(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Full Write] Done' in output
    ssd.write.assert_called_with(99, '0xFFFFFFFF')


def test_shell_fullwrite_invalid_input(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    ssd = mocker.Mock()

    mocker.patch('builtins.input', side_effect=['fullwrite 0 0', 'exit'])

    shell = Shell(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Full Write] ERROR' in output


def test_shell_fullwrite_exception(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    ssd = mocker.Mock()
    ssd.write.side_effect = [ValueError]

    mocker.patch('builtins.input', side_effect=['fullwrite 0xFFFFFFFF', 'exit'])

    shell = Shell(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Full Write] ERROR' in output
