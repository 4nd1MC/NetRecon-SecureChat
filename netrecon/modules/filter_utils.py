import time
from typing import Iterable

class RateLimiter:
    def __init__(self, rps: float):
        self.period = 1.0 / max(rps, 0.1)
        self._t = 0.0
    def wait(self):
        now = time.time()
        if self._t == 0.0:
            self._t = now
            return
        delta = self._t + self.period - now
        if delta > 0:
            time.sleep(delta)
        self._t = time.time()

def in_whitelist(ip: str, whitelist: Iterable[str] | None) -> bool:
    if not whitelist:
        return True
    return ip in set(whitelist)

def not_in_blacklist(ip: str, blacklist: Iterable[str] | None) -> bool:
    if not blacklist:
        return True
    return ip not in set(blacklist)