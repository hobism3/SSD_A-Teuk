import pytest
from pytest_mock import MockerFixture

from shell import Shell

EXIT_CMD = 'exit'
BUILTIN_INPUT = 'builtins.input'
VALID_WRITE_CMD = 'write 3 0xEEEEFFFF'
INVALID_MESSAGE = 'INVALID COMMAND'
WRITE_ERROR_MESSAGE = '[Write] ERROR'
WRITE_DONE_MESSAGE = '[Write] Done'


def test_shell_write_cmd_has_called(mocker: MockerFixture):
    cmd_lst = [VALID_WRITE_CMD, EXIT_CMD]
    mocker.patch(BUILTIN_INPUT, side_effect=cmd_lst)
    ssd = mocker.Mock()
    shell = Shell(ssd)

    shell.run()

    ssd.write.assert_called_once()


def test_shell_write_cmd(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    cmd_lst = [VALID_WRITE_CMD, EXIT_CMD]
    mocker.patch(BUILTIN_INPUT, side_effect=cmd_lst)
    ssd = mocker.Mock()
    shell = Shell(ssd)

    shell.run()
    captured = capsys.readouterr()
    output = captured.out

    assert WRITE_DONE_MESSAGE in output


def test_shell_write_cmd_invalid_param_count(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    cmd_lst = ['write', 'write 98', 'write 99 0xEEEEFFFF 16', EXIT_CMD]
    mocker.patch(BUILTIN_INPUT, side_effect=cmd_lst)
    ssd = mocker.Mock()
    shell = Shell(ssd)

    shell.run()
    captured = capsys.readouterr()
    output = captured.out

    assert WRITE_ERROR_MESSAGE in output


def test_shell_write_cmd_invalid_param_format(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    cmd_lst = [
        'write 100 0xEEEEFFFF',
        'write 0 0xEEEEFFFFE',
        'write 99 EEEEFFFF',
        EXIT_CMD,
    ]
    mocker.patch(BUILTIN_INPUT, side_effect=cmd_lst)
    ssd = mocker.Mock()
    shell = Shell(ssd)

    shell.run()
    captured = capsys.readouterr()
    output = captured.out

    assert WRITE_ERROR_MESSAGE in output


def test_shell_invalid_cmd(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    cmd_lst = ['writ 3 0xEEEEFFFF', 'rea 3', 'exi', EXIT_CMD]
    mocker.patch(BUILTIN_INPUT, side_effect=cmd_lst)
    ssd = mocker.Mock()
    shell = Shell(ssd)

    shell.run()
    captured = capsys.readouterr()
    output = captured.out

    assert INVALID_MESSAGE in output


@pytest.mark.timeout(1)
def test_shell_exit_cmd_breaks_loop(mocker: MockerFixture):
    mocker.patch(BUILTIN_INPUT, side_effect=[EXIT_CMD])
    ssd = mocker.Mock()
    shell = Shell(ssd)

    shell.run()
