import pytest
from pytest_mock import MockerFixture

from shell import Shell


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
