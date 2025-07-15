from shell_constants import LBA_RANGE, Hex
from shell_constants import ShellCmd as Cmd
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class Shell:
    def __init__(self, ssd=None):
        self._ssd = ssd

    def run(self):
        while True:
            try:
                cmd = input(Msg.PROMPT).strip()
                if not cmd:
                    continue
                parts = cmd.split()

                if parts[0].lower() == Cmd.WRITE:
                    if len(parts) != 3:
                        print(f'{Pre.WRITE} {Msg.ERROR}')
                        continue
                    try:
                        lba = int(parts[1])
                        data = parts[2]

                        # LBA 범위 검사 (0~99)
                        if lba not in LBA_RANGE:
                            print(f'{Pre.WRITE} {Msg.ERROR}')
                            continue

                        # 데이터 형식 검사: '0x'로 시작하고, 뒤에 정확히 8자리 16진수인지 확인
                        if not (
                            data.startswith(Hex.PREFIX)
                            and len(data) == Hex.LENGTH
                            and all(c in Hex.RANGE for c in data[2:])
                        ):
                            print(f'{Pre.WRITE} {Msg.ERROR}')
                            continue

                        self.device_write(lba, data)
                        print(f'{Pre.WRITE} {Msg.DONE}')
                    except ValueError:
                        print(f'{Pre.WRITE} {Msg.ERROR}')

                elif parts[0].lower() == Cmd.READ:
                    if len(parts) != 2:
                        print(f'{Pre.READ} {Msg.ERROR}')
                        continue
                    try:
                        lba = int(parts[1])
                        print(f'{Pre.READ} LBA: {lba}')
                        self.device_read(lba)
                        print(f'{Pre.READ} {Msg.DONE}')
                    except ValueError:
                        print(f'{Pre.READ} {Msg.ERROR}')

                elif parts[0].lower() == Cmd.EXIT:
                    break

                else:
                    print(Msg.INVALID)

            except (EOFError, KeyboardInterrupt):
                break

    def device_read(self, lba):
        return self._ssd.read(lba)

    def device_write(self, lba, data):
        self._ssd.write(lba, data)


if __name__ == '__main__':
    shell = Shell()
    shell.run()
