import os

SSD_OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'ssd_output.txt')
RUN_SSD = ['python', os.path.join(os.path.dirname(__file__), 'ssd.py')]


class ShellMsg:
    PROMPT = 'Shell> '
    HELP = """Documented commands (type help <topic>):
  write\tWrite data to an LBA
  read\tRead data from an LBA
  fullwrite\tWrite data to all LBAs
  fullread\tRead data from all LBAs
  help\tShow help for commands
  exit\tExit the shell"""
    READ_HELP = 'Invalid arguments. Usage: read <lba>'
    WRITE_HELP = 'Invalid arguments. Usage: write <lba> <hex data>'
    ERASE_HELP = 'Invalid arguments. Usage: erase <start lba> <size>'
    ERROR = 'ERROR'
    INVALID = 'INVALID COMMAND'
    DONE = 'Done'
    FAIL = 'FAIL'
    PASS = 'PASS'


class ShellCmd:
    READ = 'read'
    WRITE = 'write'
    FULLWRITE = 'fullwrite'
    FULLREAD = 'fullread'
    EXIT = 'exit'
    HELP = 'help'
    SCRIPT_1_FULL = '1_FullWriteAndReadCompare'
    SCRIPT_2_FULL = '2_PartialLBAWrite'
    SCRIPT_3_FULL = '3_WriteReadAging'
    SCRIPT_1_SHORT = '1_'
    SCRIPT_2_SHORT = '2_'
    SCRIPT_3_SHORT = '3_'
    ERASE = 'erase'


class ShellPrefix:
    READ = '[Read] '
    WRITE = '[Write] '
    FULLREAD = '[Full Read] '
    FULLWRITE = '[Full Write] '
    SCRIPT2 = '[2_PartialLBAWrite] '
    FULLWRITE = '[FullWrite] '
    FULLREAD = '[FullRead] '
    SCRIPT_1 = '[1_FullWriteAndReadCompare] '
    SCRIPT_2 = '[2_PartialLBAWrite] '
    SCRIPT_3 = '[3_WriteReadAging] '
    ERASE = '[Erase] '


LBA_RANGE = range(100)
SIZE_RANGE = range(1, 101)
MAX_LBA = 99
SCRIPT_1_STEP = 5
SCRIPT_3_ROTATE_CNT = 200


class Hex:
    RANGE = '0123456789abcdefABCDEF'
    PREFIX = '0x'
    LENGTH = 10
