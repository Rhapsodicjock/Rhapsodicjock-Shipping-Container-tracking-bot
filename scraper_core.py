from contextlib import asynccontextmanager
from typing import Optional
import asyncio

# Playwright is optional at authoring time; import lazily
async def _import_playwright():
    import importlib
    return importlib.import_module("playwright.async_api")

class ScraperCore:
    def __init__(self, headless: bool = True, proxy: Optional[str] = None, stealth: bool = False, user_agent: Optional[str] = None, timeout_ms: int = 90000):
        self.headless = headless
        self.proxy = proxy
        self.stealth = stealth
        self.user_agent = user_agent
        self.timeout_ms = timeout_ms

    @asynccontextmanager
    async def session(self):
        pw = await _import_playwright()
        async with pw.async_playwright() as p:
            browser_args = {}
            if self.proxy:
                browser_args["proxy"] = {"server": self.proxy}
            browser = await p.chromium.launch(headless=self.headless, args=[])
            context = await browser.new_context(**({"user_agent": self.user_agent} if self.user_agent else {}))
            # Optional stealth: user can pip install playwright-stealth
            if self.stealth:
                try:
                    from playwright_stealth import stealth_async
                    await stealth_async(context)
                except Exception:
                    pass
            yield context
            await context.close()
            await browser.close()
