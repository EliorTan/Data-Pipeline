"""
Main entry point for the API Data Pipeline.
"""

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from pipeline.config import parse_arguments
from pipeline.data_processing import run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    args = parse_arguments()
    
    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_pipeline,
        CronTrigger.from_crontab(args.schedule),
        args=[args.api_url, args.output_prefix, args.use_db, args.use_s3]
    )
    
    logger.info(f"Starting scheduler with cron: {args.schedule}")
    scheduler.start()

if __name__ == "__main__":
    main()