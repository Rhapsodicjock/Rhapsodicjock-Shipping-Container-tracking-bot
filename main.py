import asyncio
import os
from dotenv import load_dotenv
from tracker.cli import build_parser
from tracker.logger_setup import setup_logging
from tracker.config_loader import load_config, load_containers
from tracker.proxy_manager import ProxyManager
from tracker.captcha_solver import CaptchaSolver
from tracker.scraper_core import ScraperCore
from tracker.dispatcher import get_carrier
from tracker.data_extractor import parse_result
from tracker.export_manager import ExportManager
from tracker.retry_manager import get_failed
from tracker.scheduler import run_daily
from tracker.models import TrackingResult

async def track_container(q, context, args, timeout_ms):
    try:
        carrier_cls = get_carrier(q.carrier)
        carrier = carrier_cls(context=context, timeout_ms=timeout_ms)
        if args.dry_run:
            raw = await carrier.track(q.container_no)
        else:
            raw = await carrier.track(q.container_no)
        res = parse_result(q.container_no, q.carrier, raw)
        return res
    except Exception as e:
        # Add more context to the error
        print(f"Error tracking {q.container_no} ({q.carrier}): {e}")
        return None

async def run_once(args):
    logger = setup_logging()
    cfg = load_config(args.config)
    containers = load_containers(cfg)
    # ... (setup code remains unchanged)

    results = []
    core = ScraperCore(headless=headless, proxy=proxy, stealth=stealth, user_agent=user_agent, timeout_ms=timeout_ms)
    async with core.session() as context:
        tasks = [
            track_container(q, context, args, timeout_ms)
            for q in containers
        ]
        # Gather results in parallel, with error handling
        tracked = await asyncio.gather(*tasks)
        results = [res for res in tracked if res is not None]

    exporter.export(results)
    # ... (rest of the function remains unchanged)

def main():
    args = build_parser().parse_args()
    if args.schedule:
        def job():
            asyncio.run(run_once(args))
        run_daily(args.schedule, job)
    else:
        asyncio.run(run_once(args))

if __name__ == "__main__":
    main()
