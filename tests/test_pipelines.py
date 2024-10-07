"""
Unit tests for the API Data Pipeline.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sqlite3
import json
from pathlib import Path

from pipeline.utils import validate_email, clean_and_validate_data
from pipeline.api_client import fetch_data_from_api
from pipeline.database_handler import save_to_database
from pipeline.csv_handler import save_to_csv
from pipeline.s3_handler import save_to_s3
from pipeline.config import load_config

class TestPipeline(unittest.TestCase):
    def test_validate_email(self):
        self.assertTrue(validate_email("user@example.com"))
        self.assertFalse(validate_email("invalid-email"))

    def test_clean_and_validate_data(self):
        test_data = [
            {"id": 1, "name": " John Doe ", "email": "john@example.com", "company": {"name": " Acme Inc "}},
            {"id": 2, "name": "Jane Doe", "email": "invalid-email", "company": "Tech Corp"},
            {"id": 3, "name": "Bob Smith", "email": "bob@example.com", "company": {"name": "Global Ltd"}}
        ]
        result = clean_and_validate_data(test_data)
        self.assertEqual(len(result), 2)  # One invalid email should be filtered out
        self.assertEqual(result[0]["name"], "John Doe")  # Spaces should be stripped
        self.assertEqual(result[0]["company"], "Acme Inc")  # Spaces should be stripped

    @patch('pipeline.api_client.requests.get')
    def test_fetch_data_from_api(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1, "name": "Test User"}]
        mock_get.return_value = mock_response
        
        result = fetch_data_from_api("http://test-api.com")
        self.assertEqual(result, [{"id": 1, "name": "Test User"}])

    def test_save_to_database(self):
        test_data = [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "company": "Acme Inc"},
            {"id": 2, "name": "Jane Doe", "email": "jane@example.com", "company": "Tech Corp"}
        ]
        db_path = save_to_database(test_data, db_name='test_pipeline.db')
        
        # Verify that the database file was created
        self.assertTrue(os.path.exists(db_path))
        
        # Verify that the data was correctly inserted
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], "John Doe")
        self.assertEqual(rows[1][1], "Jane Doe")
        
        # Clean up the test database
        os.remove(db_path)

    def test_save_to_csv(self):
        test_data = [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "company": "Acme Inc"},
            {"id": 2, "name": "Jane Doe", "email": "jane@example.com", "company": "Tech Corp"}
        ]
        filename = "test_output.csv"
        save_to_csv(test_data, filename)
        
        # Verify that the CSV file was created
        self.assertTrue(os.path.exists(filename))
        
        # Verify the content of the CSV file
        with open(filename, 'r') as f:
            content = f.read()
            self.assertIn("John Doe", content)
            self.assertIn("jane@example.com", content)
        
        # Clean up the test CSV file
        os.remove(filename)

    @patch('pipeline.s3_handler.boto3.client')
    def test_save_to_s3(self, mock_s3_client):
        test_data = "Test CSV data"
        filename = "test_file.csv"
        
        mock_s3 = MagicMock()
        mock_s3_client.return_value = mock_s3
        
        save_to_s3(test_data, filename)
        
        mock_s3.put_object.assert_called_once_with(
            Body=test_data,
            Bucket=load_config()['aws']['bucket_name'],
            Key=filename
        )

    def test_load_config(self):
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertIn('api', config)
        self.assertIn('url', config['api'])

if __name__ == '__main__':
    unittest.main()