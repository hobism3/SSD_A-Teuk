from unittest.mock import mock_open

import pytest
from pytest_mock import MockerFixture

from shell import Shell
from shell_tool.shell_constants import ShellMsg as Msg


@pytest.fixture
def mock_run(mocker):
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('random.getrandbits', return_value=0xAAAABBBB)
    mocker.patch('builtins.open', mocker.mock_open(read_data='0xAAAABBBB'))
    mocker.patch('commands.write.WriteCommand._parse_result', return_value=Msg.DONE)

    return mock_run


def test_script4_call_subprocess_and_file_with_shortname(
    mocker: MockerFixture, mock_run
):
    mocker.patch('commands.script4.range', return_value=range(1))
    mock_open_file = mocker.patch('builtins.open', mock_open(read_data=''))
    mocker.patch('builtins.input', side_effect=['4_', 'exit'])

    shell = Shell()
    shell.run()

    assert mock_run.called
    assert mock_open_file.called
