import argparse

def build_parser():
    p = argparse.ArgumentParser(description="Shipping Container Tracking Bot")
    p.add_argument("--config", default="configs/config.yaml", help="Path to YAML config")
    p.add_argument("--headless", action="store_true", help="Run headless browser")
    p.add_argument("--retries", type=int, default=None, help="Override retry count")
    p.add_argument("--only-failed", action="store_true", help="Re-run only failed containers")
    p.add_argument("--schedule", type=str, default=None, help='Daily schedule time, e.g., "09:00"')
    p.add_argument("--dry-run", action="store_true", help="Skip real scraping and return mock data")
    return p
