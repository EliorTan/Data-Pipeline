"""
API client for the Data Pipeline.
"""

import logging
from typing import Dict, List, Optional

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def fetch_data_from_api(url: str) -> Optional[List[Dict]]:
    logger.info(f"Attempting to fetch data from: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetched data. Number of records: {len(data)}")
        return data
    except RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
        return None