import pytest
from pytest_mock import MockerFixture

from shell.shell import Shell


def test_shell_read(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    ssd.read.side_effect = ['0x00000001']

    mocker.patch('builtins.input', side_effect=['read 0', 'exit'])

    shell = Shell()
    shell.init(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Read] LBA: 0' in output
    assert '0x00000001' in output
    assert '[Read] Done' in output


def test_shell_read_invalid_input(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()

    mocker.patch('builtins.input', side_effect=['read 0 0 0', 'exit'])

    shell = Shell()
    shell.init(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Read] ERROR' in output


def test_shell_read_exception(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    ssd.read.side_effect = [ValueError]

    mocker.patch('builtins.input', side_effect=['read 0', 'exit'])

    shell = Shell()
    shell.init(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Read] ERROR' in output
