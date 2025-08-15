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

async def run_once(args):
    logger = setup_logging()
    cfg = load_config(args.config)
    containers = load_containers(cfg)

    if args.only_failed:
        logger.info("Only-failed mode: looking for previous failed list (not implemented, using all)…")

    # Settings
    settings = cfg.settings or {{}}
    headless = args.headless or settings.get("headless", True)
    retries = args.retries if args.retries is not None else settings.get("retries", 2)
    timeout_ms = settings.get("default_timeout_ms", 90000)
    stealth = settings.get("stealth", False)
    user_agent = settings.get("user_agent")

    # Infra
    load_dotenv()
    proxy = ProxyManager().get()
    captcha = CaptchaSolver()

    # Export
    exp_cfg = cfg.export or {{}}
    exporter = ExportManager(
        out_dir=exp_cfg.get("out_dir", "outputs"),
        formats=exp_cfg.get("formats", ["excel"]),
        excel_filename=exp_cfg.get("excel_filename", "tracking_results.xlsx"),
        csv_filename=exp_cfg.get("csv_filename", "tracking_results.csv"),
        json_filename=exp_cfg.get("json_filename", "tracking_results.json"),
    )

    results = []

    core = ScraperCore(headless=headless, proxy=proxy, stealth=stealth, user_agent=user_agent, timeout_ms=timeout_ms)
    async with core.session() as context:
        pages = []
        for q in containers:
            carrier_cls = get_carrier(q.carrier)
            carrier = carrier_cls(context=context, timeout_ms=timeout_ms)

            if args.dry_run:
                raw = await carrier.track(q.container_no)  # uses mock in stub
            else:
                raw = await carrier.track(q.container_no)  # replace with real logic

            res = parse_result(q.container_no, q.carrier, raw)
            results.append(res)

    exporter.export(results)

    # Failed extraction
    failed = get_failed(results)
    if failed:
        from pandas import DataFrame
        os.makedirs("outputs", exist_ok=True)
        DataFrame([f.model_dump() for f in failed]).to_excel("outputs/failed_for_retry.xlsx", index=False)

    return results

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
