from unittest.mock import call, mock_open

import pytest
from pytest_mock import MockerFixture

from shell import Shell
from shell_constants import RUN_SSD
from shell_constants import ShellCmd as Cmd


@pytest.fixture
def mock_run(mocker):
    mock_process = mocker.Mock()
    mock_process.returncode = 0

    # subprocess.run을 포함한 patch 설정
    mock_run = mocker.patch('subprocess.run', return_value=mock_process)
    mocker.patch('builtins.open', mocker.mock_open(read_data=''))

    return mock_run


def case_list(test_args_list):
    test_cases = []
    for cmd, code, value in test_args_list:
        cmd_args = RUN_SSD + [cmd, code]
        if value is not None:
            cmd_args.append(value)

        test_cases.append(call(cmd_args, check=True))

    return test_cases


def test_erase_call_subprocess_and_file(mocker: MockerFixture, mock_run):
    mock_open_file = mocker.patch('builtins.open', mock_open(read_data=''))
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE} 0 1', Cmd.EXIT])

    shell = Shell()
    shell.run()

    assert mock_run.called
    assert mock_open_file.called


def test_erase_pass_with_no_include_any_error(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.open', mock_open(read_data=''))
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE} 0 3', Cmd.EXIT])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert '[Erase]' in output and 'Done' in output
    assert 'ERROR' not in output


def test_erase_invalid_param_count(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE} 0 1 1', Cmd.EXIT])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert 'ERROR' in output
    assert 'Done' not in output


def test_erase_invalid_command(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE}e 0 1 1', Cmd.EXIT])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert 'INVALID COMMAND' in output
    assert 'Done' not in output


def test_erase_invalid_lba_range(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE} 100 1 ', Cmd.EXIT])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert 'ERROR' in output
    assert 'Done' not in output


def test_erase_invalid_size(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE} 0 101 ', Cmd.EXIT])

    shell = Shell()
    shell.run()

    captured = capsys.readouterr()
    output = captured.out
    assert 'ERROR' in output
    assert 'Done' not in output


def test_erase_valid_call_args_all_list(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE} 0 100 ', Cmd.EXIT])
    test_args_list = [('E', str(i), '10') for i in range(0, 100, 10)]
    split_case = case_list(test_args_list)

    shell = Shell()
    shell.run()

    for case in split_case:
        assert case in mock_run.call_args_list


def test_erase_valid_call_args_unaligned_list(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE} 0 98 ', Cmd.EXIT])
    test_args_list = [('E', str(i), '10') for i in range(0, 90, 10)] + [
        ('E', '90', '8')
    ]
    split_case = case_list(test_args_list)

    shell = Shell()
    shell.run()

    for case in split_case:
        assert case in mock_run.call_args_list


def test_erase_valid_call_args_all_list_valid_order(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE} 0 100 ', Cmd.EXIT])
    test_args_list = [('E', str(i), '10') for i in range(0, 100, 10)]
    split_case = case_list(test_args_list)

    shell = Shell()
    shell.run()

    mock_run.assert_has_calls(split_case, any_order=False)


def test_erase_call_args_unaligned_list_valid_order(
    capsys: pytest.CaptureFixture, mocker: MockerFixture, mock_run
):
    mocker.patch('builtins.input', side_effect=[f'{Cmd.ERASE} 0 98 ', Cmd.EXIT])
    test_args_list = [('E', str(i), '10') for i in range(0, 90, 10)] + [
        ('E', '90', '8')
    ]
    split_case = case_list(test_args_list)

    shell = Shell()
    shell.run()

    mock_run.assert_has_calls(split_case, any_order=False)
