class Buffer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        ...

    def buffer_file_read(self) -> list:
        ...

    def buffer_file_write(self, lst):
        ...

    def _write(self, address, new_content):
        ...

    def _read(self, address):
        ...

    def _erase(self):
        ...
