# utils/rate_limiter.py
import time
from collections import deque
from functools import wraps

class RateLimiter:
    """
    Simple sliding-window rate limiter.
    default: 30 calls / 60 seconds
    """
    def __init__(self, max_calls: int = 30, period: int = 60):
        self.max_calls = max_calls
        self.period    = period
        self.calls     = deque()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # remove outdated timestamps
            while self.calls and self.calls[0] <= now - self.period:
                self.calls.popleft()
            if len(self.calls) >= self.max_calls:
                sleep_time = self.calls[0] + self.period - now
                time.sleep(sleep_time)
            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    
    