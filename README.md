# Shipping Tracker Bot (Scaffold)

Production-ready scaffold for a modular shipping container tracking bot using Playwright (with optional stealth), retries, proxy rotation, and scheduled runs.

## Quickstart

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt

# (Optional) Install Playwright browsers
python -m playwright install

# Copy example config and env
cp configs/config.example.yaml configs/config.yaml
cp .env.example .env

# Try a dry run (no scraping)
python main.py --dry-run --headless

# Run normally
python main.py --headless --retries 2
```

## Features
- Modular per-carrier scrapers (MSC, PIL, Maersk as examples)
- Playwright-based ScraperCore with optional stealth
- Retry with exponential backoff
- Proxy rotation hooks
- CAPTCHA solver hook (e.g., 2captcha/anticaptcha)
- Scheduler (daily at a time, e.g., 09:00) via `--schedule 09:00`
- Exports: Excel/CSV/JSON
- Logs to file and console
- "Only failed" re-run support

> This scaffold includes safe placeholder scrapers that return mock data. Replace them with real selectors/flows per carrier.
