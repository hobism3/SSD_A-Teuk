class Shell:
    def __init__(self, ssd=None):
        self._ssd = ssd

    def run(self):
        while True:
            try:
                cmd = input('Shell> ').strip()
                if not cmd:
                    continue
                parts = cmd.split()

                if parts[0].lower() == 'write':
                    if len(parts) != 3:
                        print('[Write] ERROR')
                        continue
                    try:
                        lba = int(parts[1])
                        data = parts[2]

                        # LBA 범위 검사 (0~99)
                        if not (0 <= lba < 100):
                            print('[Write] ERROR')
                            continue

                        # 데이터 형식 검사: '0x'로 시작하고, 뒤에 정확히 8자리 16진수인지 확인
                        if not (
                            data.startswith('0x')
                            and len(data) == 10
                            and all(c in '0123456789abcdefABCDEF' for c in data[2:])
                        ):
                            print('[Write] ERROR')
                            continue

                        self._ssd.write(lba, data)
                        print('[Write] Done')
                    except ValueError:
                        print('[Write] ERROR')

                elif parts[0].lower() == 'read':
                    if len(parts) != 2:
                        print('[Read] ERROR')
                        continue
                    try:
                        lba = int(parts[1])
                        print(f'[Read] LBA {lba:02d}: {self._ssd.read(lba)}')
                    except ValueError:
                        print('[Read] ERROR')

                elif parts[0].lower() == 'fullread':
                    if len(parts) != 1:
                        print('[Full Read] ERROR')
                        continue
                    try:
                        print('[Full Read]')
                        for lba in range(100):
                            print(f'LBA {lba:02d} : {self._ssd.read(lba)}')

                    except ValueError:
                        print('[Full Read] ERROR')

                elif parts[0].lower() == 'fullwrite':
                    if len(parts) != 2:
                        print('[Full Write] ERROR')
                        continue
                    try:
                        for lba in range(100):
                            self._ssd.write(lba, parts[1])
                        print('[Full Write] Done')
                    except ValueError:
                        print('[Full Write] ERROR')

                elif parts[0].lower() == 'exit':
                    break

                else:
                    print('INVALID COMMAND')

            except (EOFError, KeyboardInterrupt):
                break


if __name__ == '__main__':
    shell = Shell()
    shell.run()
