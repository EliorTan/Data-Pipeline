"""
Utility functions for the API Data Pipeline.
"""

import re
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

def validate_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def clean_and_validate_data(data: List[Dict]) -> List[Dict]:
    cleaned_data = []
    for user in data:
        if not all(key in user for key in ['id', 'name', 'email', 'company']):
            logger.warning(f"Skipping user due to missing fields: {user}")
            continue
        
        email = user['email'].strip().lower()
        if not validate_email(email):
            logger.warning(f"Invalid email for user {user['id']}: {email}")
            continue
        
        cleaned_data.append({
            "id": user["id"],
            "name": user["name"].strip(),
            "email": email,
            "company": user["company"]["name"].strip() if isinstance(user["company"], dict) else str(user["company"]).strip()
        })
    return cleaned_data