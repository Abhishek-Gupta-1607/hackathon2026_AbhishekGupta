import random
import time

def safe_tool_call(func, *args, retries=2, **kwargs):
    """Executes a tool call with built-in retry logic."""
    for i in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if i == retries - 1:
                raise e
            time.sleep(1) # wait before retry

def simulate_failure():
    """Simulates a random API failure."""
    if random.random() < 0.2: # 20% chance to fail
        raise TimeoutError("API Timeout")
