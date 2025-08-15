import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class RetryableError(Exception):
    pass

def retry_policy(max_attempts=3):
    return retry(
        reraise=True,
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(RetryableError),
    )
