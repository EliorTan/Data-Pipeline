"""
Unit tests for the API Data Pipeline.
"""

import unittest
from unittest.mock import patch, MagicMock

from pipeline.utils import validate_email, clean_and_validate_data
from pipeline.api_client import fetch_data_from_api

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

if __name__ == '__main__':
    unittest.main()