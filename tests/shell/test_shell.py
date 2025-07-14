from pytest_mock import MockerFixture

from shell import Shell


def test_shell_write_cmd_has_called(mocker: MockerFixture):
    ssd = mocker.Mock()
    mocker.patch('builtins.input', side_effect=['write 3 0xEEEEFFFF', 'exit'])
    shell = Shell(ssd)

    shell.run()

    ssd.write.assert_called_once()
