# API Data Pipeline

This project implements a data pipeline that fetches user data from an API, processes it, and saves it to a CSV file.


## Installation

1. Clone this repository
2. Install the required packages:# API Data Pipeline

## Overview

This project implements a robust data pipeline that fetches user data from an API, processes it, and saves it to a CSV file. It demonstrates best practices in Python programming, data engineering, and ETL (Extract, Transform, Load) processes.

## Features

- Fetches data from a configurable API endpoint
- Cleans and validates the fetched data
- Saves processed data to CSV files
- Implements scheduled execution using APScheduler
- Provides comprehensive logging
- Includes unit tests for key components

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```
   git clone "Repo URL"
   cd data-engineer
   ```


2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the pipeline with default settings:

```
python main.py
```

This will start the scheduler, which will run the pipeline according to the default schedule (hourly).

### Advanced Usage

Customize the pipeline run with command-line arguments:

```
python main.py --api-url "https://jsonplaceholder.typicode.com/users" --schedule "*/1 * * * *"
```

- `--api-url`: Set the API endpoint to fetch data from
- `--output-prefix`: Set the prefix for output CSV files
- `--schedule`: Set the cron schedule for pipeline execution

### Output

The pipeline creates CSV files in the project root directory with the naming pattern:
```
{output_prefix}_{YYYYMMDD_HHMMSS}.csv
```

## Project Structure

- `main.py`: Entry point of the application
- `pipeline/`: Contains the core pipeline modules
  - `config.py`: Configuration and argument parsing
  - `api_client.py`: Handles API interactions
  - `data_processing.py`: Data processing and pipeline logic
  - `utils.py`: Utility functions for data cleaning and validation
- `tests/`: Contains unit tests
- `requirements.txt`: List of Python package dependencies

## Running Tests

To run the unit tests:

```
python -m unittest discover tests
```

## Logging

The pipeline logs its activities to both the console and a file named `pipeline.log` in the project root directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Requests](https://docs.python-requests.org/) for API interactions
- [pandas](https://pandas.pydata.org/) for data manipulation
- [APScheduler](https://apscheduler.readthedocs.io/) for task scheduling