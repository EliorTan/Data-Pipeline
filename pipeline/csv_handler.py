"""
CSV handling operations for the API Data Pipeline.
"""
import logging
from typing import List, Dict, Optional
import pandas as pd

logger = logging.getLogger(__name__)

def save_to_csv(data: List[Dict], filename: str, return_data: bool = False) -> Optional[str]:
    df = pd.DataFrame(data)
    if return_data:
        return df.to_csv(index=False)
    else:
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")
    return None