"""
Main data processing logic for the API Data Pipeline.
"""
import logging
from datetime import datetime
from typing import List, Dict

from pipeline.api_client import fetch_data_from_api
from pipeline.utils import clean_and_validate_data
from pipeline.csv_handler import save_to_csv
from pipeline.s3_handler import save_to_s3
from pipeline.database_handler import save_to_database

logger = logging.getLogger(__name__)

def run_pipeline(api_url: str, output_prefix: str, use_db: bool = False, use_s3: bool = False):
    logger.info(f"Starting data pipeline with API URL: {api_url}")
    
    raw_data = fetch_data_from_api(api_url)
    if raw_data is None:
        logger.error("Failed to fetch data. Aborting pipeline.")
        return
    
    logger.info(f"Fetched {len(raw_data)} records. Processing data...")
    processed_data = clean_and_validate_data(raw_data)
    
    if use_db:
        db_path = save_to_database(processed_data)
        logger.info(f"Data saved to database at: {db_path}")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_prefix}_{timestamp}.csv"
        
        if use_s3:
            csv_data = save_to_csv(processed_data, output_file, return_data=True)
            if csv_data:
                save_to_s3(csv_data, output_file)
        else:
            save_to_csv(processed_data, output_file)
    
    logger.info("Data pipeline completed successfully")