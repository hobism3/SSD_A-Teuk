import pytest

from pytest_mock import MockerFixture

from shell import Shell


def test_shell_write_cmd_has_called(mocker: MockerFixture):
    ssd = mocker.Mock()
    shell = Shell(ssd)
    mocker.patch('builtins.input', side_effect=['write 3 0xEEEEFFFF', 'exit'])

    shell.run()

    ssd.write.assert_called_once()


def test_shell_write_cmd(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    mocker.patch('builtins.input', side_effect=['write 32 0xEEEEFFFF', 'exit'])
    shell = Shell(ssd)

    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Write] Done' in output


def test_shell_write_cmd_invalid_param_count(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    ssd = mocker.Mock()
    mocker.patch(
        'builtins.input',
        side_effect=['write', 'write 98', 'write 99 0xEEEEFFFF 16', 'exit'],
    )
    shell = Shell(ssd)

    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Write] ERROR' in output


def test_shell_write_cmd_invalid_param_format(
    capsys: pytest.CaptureFixture, mocker: MockerFixture
):
    ssd = mocker.Mock()
    mocker.patch(
        'builtins.input',
        side_effect=[
            'write 100 0xEEEEFFFF',
            'write 0 0xEEEEFFFFE',
            'write 99 EEEEFFFF',
            'exit',
        ],
    )
    shell = Shell(ssd)

    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Write] ERROR' in output


def test_shell_invalid_cmd(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    mocker.patch(
        'builtins.input', side_effect=['writ 3 0xEEEEFFFF', 'rea 3', 'exi', 'exit']
    )
    shell = Shell(ssd)

    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert 'INVALID COMMAND' in output


@pytest.mark.timeout(1)
def test_shell_exit_cmd_breaks_loop(mocker: MockerFixture):
    ssd = mocker.Mock()
    shell = Shell(ssd)
    mocker.patch('builtins.input', side_effect=['exit'])

    shell.run()
