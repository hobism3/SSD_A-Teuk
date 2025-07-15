class Logger:
    def __init__(self, prefix=''):
        self._prefix = prefix

    def info(self, message):
        self._print(message)

    def error(self, message):
        self._print(message)

    def debug(self, message):
        self._print(message, use_prefix=False)

    def _print(self, message, use_prefix=True):
        if use_prefix:
            message = ' '.join([self._prefix, message])
        print(message)
