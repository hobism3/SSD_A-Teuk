import datetime
import inspect
import os
import time

from filelock import FileLock

from shell_constants import LOG_LATEST, LOG_PATH

MAX_SIZE = 10 * 1024  # 10 KB


class Logger:
    def __init__(self, verbose=True):
        os.makedirs(LOG_PATH, exist_ok=True)
        self.filename = os.path.join(LOG_PATH, LOG_LATEST)
        self._verbose = verbose
        self._lock = FileLock(lock_file='.lock')

    def set_verbose(self, verbose):
        self._verbose = verbose

    def log(self, message: str):
        caller = self._get_caller()
        timestamp = datetime.datetime.now().strftime('%y.%m.%d %H:%M')
        log_line = f'[{timestamp}] {caller:<30}: {message}\n'
        with self._lock:
            self._rotate_log()
            with open(self.filename, 'a') as f:
                f.write(log_line)

    def dot(self):
        self.print(message='.', end='', flush=True)

    def print_blank_line(self):
        self.print()

    def print(self, prefix: str = '', message: str = '', end='\n', flush=False):
        if not self._verbose:
            return
        msg = []
        if prefix:
            msg.append(prefix)
        if message:
            msg.append(message)
        print(' '.join(msg), end=end, flush=flush)

    def print_and_log(self, prefix: str = '', message: str = ''):
        self.print(prefix, message)
        self.log(message)

    def _get_caller(self):
        for frame_info in inspect.stack():
            frame = frame_info.frame
            cls = frame.f_locals.get('self', None)
            if cls is not None and not isinstance(cls, Logger):
                class_name = cls.__class__.__name__
                method_name = frame_info.function
                return f'{class_name}.{method_name}()'
        return '(Unknown)'

    def _rotate_log(self):
        if not os.path.exists(self.filename):
            return
        if os.path.getsize(self.filename) < MAX_SIZE:
            return

        now = datetime.datetime.now().strftime('%y%m%d_%Hh_%Mm_%Ss')
        rotated_name = f'until_{now}.log'
        while os.path.exists(rotated_name):
            time.sleep(0.1)
            now = datetime.datetime.now().strftime('%y%m%d_%Hh_%Mm_%Ss')
            rotated_name = f'until_{now}.log'
        os.rename(self.filename, os.path.join(LOG_PATH, rotated_name))

        old_logs = sorted(
            [
                os.path.join(LOG_PATH, f)
                for f in os.listdir(LOG_PATH)
                if f.startswith('until_') and f.endswith('.log')
            ]
        )
        if len(old_logs) > 2:
            for f in old_logs[:-1]:
                os.rename(f, f.replace('.log', '.zip'))
