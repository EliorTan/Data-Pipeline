"""
Data processing functions for the API Data Pipeline.
"""

import logging
from datetime import datetime
from typing import Dict, List

import pandas as pd

from pipeline.api_client import fetch_data_from_api
from pipeline.utils import clean_and_validate_data

logger = logging.getLogger(__name__)

def save_to_csv(data: List[Dict], filename: str) -> None:
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    logger.info(f"Data saved to {filename}")

def run_pipeline(api_url: str, output_prefix: str) -> None:
    logger.info(f"Starting data pipeline with API URL: {api_url}")
    
    raw_data = fetch_data_from_api(api_url)
    if raw_data is None:
        logger.error("Failed to fetch data. Aborting pipeline.")
        return
    
    logger.info(f"Fetched {len(raw_data)} records. Processing data...")
    processed_data = clean_and_validate_data(raw_data)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_prefix}_{timestamp}.csv"
    logger.info(f"Saving data to {output_file}")
    save_to_csv(processed_data, output_file)
    
    logger.info("Data pipeline completed successfully")