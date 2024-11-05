"""
Configuration and argument parsing for the API Data Pipeline.
"""
import json
import argparse

def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        return json.load(f)

def parse_arguments():
    config = load_config()
    parser = argparse.ArgumentParser(description="API Data Pipeline")
    parser.add_argument("--api-url", default=config['api']['url'], help="API URL")
    parser.add_argument("--output-prefix", default=config['output']['prefix'], help="Output file prefix")
    parser.add_argument("--schedule", default=config['schedule'], help="Cron schedule")
    parser.add_argument("--use-s3", action="store_true", default=config['aws']['use_s3'], help="Store data in S3")
    parser.add_argument("--use-db", action="store_true", default=config['database']['use_db'], help="Store data in SQLite database")
    return parser.parse_args()

CONFIG = load_config()