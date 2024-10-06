"""
Configuration and argument parsing for the API Data Pipeline.
"""

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="API Data Pipeline")
    parser.add_argument("--api-url", default="https://jsonplaceholder.typicode.com/users", help="API URL")
    parser.add_argument("--output-prefix", default="user_data", help="Output file prefix")
    parser.add_argument("--schedule", default="0 * * * *", help="Cron schedule (default: hourly)")
    return parser.parse_args()