import pytest
from pytest_mock import MockerFixture

from shell import Shell
from shell_constants import ShellCmd as Cmd
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre

INPUT_FUNCTION = 'builtins.input'


def test_shell_write_cmd_has_called(mocker: MockerFixture):
    ssd = mocker.Mock()
    shell = Shell(ssd)
    mocker.patch(INPUT_FUNCTION, side_effect=[f'{Cmd.WRITE} 3 0xEEEEFFFF', Cmd.EXIT])

    shell.run()

    ssd.write.assert_called_once()


def test_shell_write_cmd(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    mocker.patch(INPUT_FUNCTION, side_effect=[f'{Cmd.WRITE} 32 0xEEEEFFFF', Cmd.EXIT])
    shell = Shell(ssd)

    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert Msg.DONE in output
    assert Pre.WRITE in output


def test_shell_write_cmd_invalid_param_count(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    ssd = mocker.Mock()
    mocker.patch(
        INPUT_FUNCTION,
        side_effect=[
            Cmd.WRITE,
            f'{Cmd.WRITE} 98',
            f'{Cmd.WRITE} 99 0xEEEEFFFF 16',
            Cmd.EXIT,
        ],
    )
    shell = Shell(ssd)

    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert Msg.ERROR in output
    assert Pre.WRITE in output


def test_shell_write_cmd_invalid_param_format(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    ssd = mocker.Mock()
    mocker.patch(
        INPUT_FUNCTION,
        side_effect=[
            f'{Cmd.WRITE} 100 0xEEEEFFFF',
            f'{Cmd.WRITE} 0 0xEEEEFFFFE',
            f'{Cmd.WRITE} 99 EEEEFFFF',
            Cmd.EXIT,
        ],
    )
    shell = Shell(ssd)

    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert Msg.ERROR in output
    assert Pre.WRITE in output


def test_shell_invalid_cmd(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    mocker.patch(
        INPUT_FUNCTION, side_effect=['writ 3 0xEEEEFFFF', 'rea 3', 'exi', Cmd.EXIT]
    )
    shell = Shell(ssd)

    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert Msg.INVALID in output


@pytest.mark.timeout(1)
def test_shell_exit_cmd_breaks_loop(mocker: MockerFixture):
    ssd = mocker.Mock()
    shell = Shell(ssd)
    mocker.patch(INPUT_FUNCTION, side_effect=[Cmd.EXIT])

    shell.run()
