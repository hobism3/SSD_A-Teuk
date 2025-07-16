import datetime
import inspect
import os
from threading import Lock

LOG_FILE = 'latest.log'
MAX_SIZE = 10 * 1024  # 10 KB


class Logger:
    def __init__(self, verbose=True):
        self.filename = LOG_FILE
        self._verbose = verbose
        self._lock = Lock()

    def set_verbose(self, verbose):
        self._verbose = verbose

    def log(self, message: str):
        self._rotate_log()
        caller = self._get_caller()
        timestamp = datetime.datetime.now().strftime('%y.%m.%d %H:%M')
        log_line = f'[{timestamp}] {caller:<30}: {message}\n'
        with self._lock:
            with open(self.filename, 'a') as f:
                f.write(log_line)

    def dot(self):
        self.print(None, '.', end='', flush=True)

    def print_blank_line(self):
        self.print(None, '')

    def print(self, prefix: str, message: str, end='\n', flush=False):
        if not self._verbose:
            return
        msg = []
        if prefix:
            msg.append(prefix)
        if message:
            msg.append(message)
        print(' '.join(msg), end=end, flush=flush)

    def print_and_log(self, tag: str, message: str):
        self.print(tag, message)
        self.log(message)

    def _get_caller(self):
        frame = inspect.currentframe()
        outer = inspect.getouterframes(frame)[2]
        method = outer.function
        cls = outer.frame.f_locals.get('self', None)
        class_name = cls.__class__.__name__ if cls else '(NoClass)'
        return f'{class_name}.{method}()'

    def _rotate_log(self):
        if not os.path.exists(self.filename):
            return
        if os.path.getsize(self.filename) < MAX_SIZE:
            return

        now = datetime.datetime.now().strftime('until_%y%m%d_%Hh_%Mm_%Ss')
        rotated_name = f'until_{now}.log'
        with self._lock:
            os.rename(self.filename, rotated_name)

        old_logs = sorted(
            [
                f
                for f in os.listdir('.')
                if f.startswith('until_') and f.endswith('.log')
            ]
        )
        if len(old_logs) > 2:
            oldest = old_logs[0]
            os.rename(oldest, oldest.replace('.log', '.zip'))
