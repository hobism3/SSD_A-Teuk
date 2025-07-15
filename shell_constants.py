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
    ERROR = 'ERROR'
    INVALID = 'INVALID COMMAND'
    DONE = 'Done'


class ShellCmd:
    READ = 'read'
    WRITE = 'write'
    FULLWRITE = 'fullwrite'
    FULLREAD = 'fullread'
    EXIT = 'exit'
    HELP = 'help'


class ShellPrefix:
    READ = '[Read] '
    WRITE = '[Write] '


LBA_RANGE = range(100)


class Hex:
    RANGE = '0123456789abcdefABCDEF'
    PREFIX = '0x'
    LENGTH = 10
