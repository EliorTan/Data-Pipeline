"""
S3 operations for the API Data Pipeline.
"""
import logging
import boto3
from botocore.exceptions import ClientError
from pipeline.config import CONFIG

logger = logging.getLogger(__name__)

def save_to_s3(data: str, filename: str):
    s3_client = boto3.client('s3', region_name=CONFIG['aws']['region'])
    try:
        s3_client.put_object(Body=data, Bucket=CONFIG['aws']['bucket_name'], Key=filename)
        logger.info(f"Data saved to S3: {filename}")
    except ClientError as e:
        logger.error(f"Error saving data to S3: {e}")