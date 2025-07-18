import os
import sys

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SSD_OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'ssd_output.txt')
PYTHON = sys.executable
RUN_SSD = [PYTHON, os.path.join(OUTPUT_DIR, 'ssd.py')]
LOG_PATH = os.path.join(OUTPUT_DIR, 'log')
LOG_LATEST = 'latest.log'

LBA_RANGE = range(100)
SIZE_RANGE = range(1, 101)
MAX_LBA = 99
RANGE_32BIT = range(0x100000000)


class Hex:
    RANGE = '0123456789abcdefABCDEF'
    PREFIX = '0x'
    LENGTH = 10


class ShellMsg:
    PROMPT = 'Shell> '
    HELP = """Documented commands (type help <topic>):
▷ Basic Commands
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
write [lba] [val]         -   writes a val on lba (ex. write 10 0x1234ABCD)
read [lba]                -   reads the val written on lba (ex. read 10)
exit                      -   exits program
help                      -   prints manual to stdout
fullwrite [val]           -   writes val to all lbas ranging from 0 to 99
fullread                  -   reads all vals written on each lba ranging from 0 to 99 and prints to stdout
erase [lba] [size]        -   wipes ssd 'size' amount of lbas starting from lba
erase_range [slba] [elba] -   wipes ssd lbas in range [slba, elba]
flush                     -   executes and clears all buffered commands (run with "flush" or "F")
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
▶ Script Commands
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
1_FullWriteAndReadCompare  -  writes/verifies random vals in 5-LBA blocks across full range; PASS/FAIL (run "1_")
2_PartialLBAWrite          -  writes/verifies same val to LBAs 0-4, 30 times; PASS/FAIL (run "2_")
3_WriteReadAging           -  writes/verifies same val to LBAs 0 and 99, 200 times; PASS/FAIL (run "3_")
4_EraseAndWriteAging       -  erases/writes vals in overlapping LBA ranges, 30 times; PASS/FAIL (run "4_")
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  """
    READ_HELP = 'Invalid arguments. Usage: read <lba>'
    WRITE_HELP = 'Invalid arguments. Usage: write <lba> <hex data>'
    FLUSH_HELP = 'Invalid arguments. Usage: flush'
    FULLREAD_HELP = 'Invalid arguments. Usage: fullread'
    FULLWRITE_HELP = 'Invalid arguments. Usage: fullwrite'
    SCRIPT_1_HELP = 'Invalid arguments. Usage: 1_FullWriteAndReadCompare or 1_'
    SCRIPT_2_HELP = 'Invalid arguments. Usage: 2_PartialLBAWrite or 2_'
    SCRIPT_3_HELP = 'Invalid arguments. Usage: 3_WriteReadAging or 3_'
    SCRIPT_4_HELP = 'Invalid arguments. Usage: 4_EraseAndWriteAging or 4_'
    ERASE_HELP = 'Invalid arguments. Usage: erase <start lba> <size>'
    ERASE_RANGE_HELP = 'Invalid arguments. Usage: erase_range <start lba> <end lba>'
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
    FLUSH = 'flush'
    ERASE = 'erase'
    ERASERANGE = 'erase_range'
    SCRIPT_1_FULL = '1_FullWriteAndReadCompare'
    SCRIPT_2_FULL = '2_PartialLBAWrite'
    SCRIPT_3_FULL = '3_WriteReadAging'
    SCRIPT_4_FULL = '4_EraseAndWriteAging'
    SCRIPT_1_SHORT = '1_'
    SCRIPT_2_SHORT = '2_'
    SCRIPT_3_SHORT = '3_'
    SCRIPT_4_SHORT = '4_'


class ShellPrefix:
    READ = '[Read]'
    WRITE = '[Write]'
    FLUSH = '[Flush]'
    ERASE = '[Erase]'
    ERASERANGE = '[Erase Range] '
    FULLREAD = '[Full Read]'
    FULLWRITE = '[Full Write]'
    FULLWRITE = '[FullWrite]'
    FULLREAD = '[FullRead]'
    SCRIPT_1 = '[1_FullWriteAndReadCompare]'
    SCRIPT_2 = '[2_PartialLBAWrite]'
    SCRIPT_3 = '[3_WriteReadAging]'
    SCRIPT_4 = '[4_EraseAndWriteAging]'


SCRIPT_1_STEP = 5
SCRIPT_3_ROTATE_CNT = 200


class Script4:
    DEFAULT_ERASE_SIZE = 3
    STEP_LBA = 2
    LOOP1 = 30
    LOOP2 = 49
