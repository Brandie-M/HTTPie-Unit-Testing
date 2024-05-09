import subprocess
import unittest
from unittest.mock import patch

# These unittests simulate error handling scenarios when sending HTTP requests with HTTPie.
# Use the following command to install HTTPie if it's not already installed:
# pip install httpie

# Use the following command to run the test:
# python -m unittest test_error_handling.py

class TestHTTPieErrorHandling(unittest.TestCase):
    # The setUp method is called before each test in this class.
    def setUp(self):
        self.url = 'http://localhost:3000/error'

    @patch('subprocess.run')
    def test_404_not_found(self, mock_run):
        # Simulate a 404 Not Found error response
        mock_run.return_value.stdout = "HTTP/1.1 404 Not Found"
        mock_run.return_value.returncode = 0  # HTTPie exits with 0 even on HTTP errors
        command = f'http --verbose GET {self.url}'
        result = self.run_httpie(command)
        self.assertIn("404 Not Found", result.stdout)
        self.assertEqual(result.returncode, 0)

    @patch('subprocess.run')
    def test_500_internal_server_error(self, mock_run):
        # Simulate a 500 Internal Server Error
        mock_run.return_value.stdout = "HTTP/1.1 500 Internal Server Error"
        mock_run.return_value.returncode = 0
        command = f'http --verbose GET {self.url}'
        result = self.run_httpie(command)
        self.assertIn("500 Internal Server Error", result.stdout)

    @patch('subprocess.run')
    def test_timeout_error(self, mock_run):
        # Simulate a network timeout error
        mock_run.return_value.stderr = "http: error: Request timed out"
        mock_run.return_value.returncode = 2  # Simulating non-zero exit code for timeouts
        command = f'http --timeout=1 GET {self.url}'
        result = self.run_httpie(command)
        self.assertIn("Request timed out", result.stderr)
        self.assertNotEqual(result.returncode, 0)

    def run_httpie(self, command):
        # Helper function to run HTTPie commands
        return subprocess.run(command, shell=True, text=True, capture_output=True)

if __name__ == '__main__':
    unittest.main()
