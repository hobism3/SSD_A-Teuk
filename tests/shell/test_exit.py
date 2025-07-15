import pytest
from pytest_mock import MockerFixture

from shell import Shell


@pytest.mark.timeout(1)
def test_shell_exit_cmd_breaks_loop(mocker: MockerFixture):
    ssd = mocker.Mock()
    shell = Shell(ssd)
    mocker.patch('builtins.input', side_effect=['exit'])

    shell.run()
