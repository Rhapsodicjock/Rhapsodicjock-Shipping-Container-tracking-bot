import os
from itertools import cycle
from typing import Optional

class ProxyManager:
    def __init__(self, proxy_pool_env: str = "PROXY_POOL"):
        proxies = os.getenv(proxy_pool_env, "")
        self.pool = [p.strip() for p in proxies.split(",") if p.strip()]
        self._cycler = cycle(self.pool) if self.pool else None

    def get(self) -> Optional[str]:
        if not self._cycler:
            return None
        return next(self._cycler)
