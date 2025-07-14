class Shell:
    def init(self, ssd=None):
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
                        print(f'[Write] LBA: {lba}, Data: {data}')
                        ## Write 동작
                        ## --------
                        print('[Write] Done')
                    except ValueError:
                        print('[Write] ERROR')

                elif parts[0].lower() == 'read':
                    if len(parts) != 2:
                        print('[Read] ERROR')
                        continue
                    try:
                        lba = int(parts[1])
                        print(f'[Read] LBA: {lba}')
                        ## Read 동작
                        ## --------
                        print('[Read] Done')
                    except ValueError:
                        print('[Read] ERROR')

                elif parts[0].lower() == 'exit':
                    break

                else:
                    print('INVALID COMMAND')

            except (EOFError, KeyboardInterrupt):
                break


if __name__ == '__main__':
    shell = Shell()
    shell.run()
