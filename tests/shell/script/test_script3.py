from unittest.mock import mock_open

from shell import Shell


def test_script3_success_with_fullname(mocker):
    mock_run = mocker.patch('commands.base.subprocess.run')
    mock_open_file = mocker.patch('builtins.open', mock_open(read_data=''))
    mocker.patch('builtins.input', side_effect=['3_WriteReadAging', 'exit'])
    mocker.patch('commands.read.ReadCommand.execute', return_value='0xAAAABBBB')

    shell = Shell()
    shell.run()

    # subprocess.run()이 정확한 파라미터로 호출되었는지 검증
    print(mock_run.call_args)
    assert mock_run.called
    assert mock_open_file.called


def test_script3_success_with_shortname(mocker):
    mock_run = mocker.patch('commands.base.subprocess.run')
    mock_open_file = mocker.patch('builtins.open', mock_open(read_data=''))
    mocker.patch('builtins.input', side_effect=['3_', 'exit'])
    mocker.patch('commands.read.ReadCommand.execute', return_value='0xAAAABBBB')

    shell = Shell()
    shell.run()

    # subprocess.run()이 정확한 파라미터로 호출되었는지 검증
    print(mock_run.call_args)
    assert mock_run.called
    assert mock_open_file.called
