from typing import Callable


class Validator:
    def __init__(self, fn: Callable, indexes: tuple[int]):
        self.fn = fn
        self.indexes = indexes

    def validate(self, args: list[str]):
        values = [args[i] for i in self.indexes]
        self.fn(*values)
