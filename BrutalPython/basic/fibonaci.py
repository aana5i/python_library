from functools import lru_cache


class Fib:
    def __init__(self, n):
        self._n = n

    def __len__(self):
        return self._n

    def __getitem__(self, item):
        if isinstance(item, int):
            if item < 0:
                item = self._n + item
            if item < 0 or item >= self._n:
                raise IndexError
            else:
                return self._fib(item)

    @lru_cache(2*10)
    def _fib(self, n):
        if n < 2:
            return 1
        else:
            return self._fib(n-1) + self._fib(n-2)


fib = Fib(20)
print(list(fib))
