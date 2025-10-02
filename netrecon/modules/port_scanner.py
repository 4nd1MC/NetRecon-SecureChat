import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from .filter_utils import RateLimiter

def scan_tcp_connect(host: str, ports: list[int], workers: int = 200, rps: float = 500.0, timeout: float = 1.0):
    limiter = RateLimiter(rps)
    results = {}
    def check(p):
        limiter.wait()
        try:
            with socket.create_connection((host, p), timeout=timeout):
                return p, "open"
        except socket.timeout:
            return p, "filtered"
        except Exception:
            return p, "closed"
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(check, p) for p in ports]
        for f in as_completed(futs):
            p, st = f.result()
            results[p] = st
    return dict(sorted(results.items()))