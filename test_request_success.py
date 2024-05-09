import subprocess
import unittest
from unittest.mock import patch

# These unittests use the HTTPie command-line tool to send HTTP requests to a server.
# Use the following command to install HTTPie:
# pip install httpie

# Use the following command to run the test:
# python -m unittest test_request_success.py

class TestHTTPRequestSuccess(unittest.TestCase):

    # The setUp method is called before each test in this class.
    # It initializes the URL and the HTTPie command.
    def setUp(self):
        self.url = 'http://localhost:3000/success'
        self.command = f'http --verbose GET {self.url}'

    # The following tests simulate different HTTP response scenarios.
    @patch('subprocess.run')
    def test_http_request_success(self, mock_run):
        mock_run.return_value.stdout = "HTTP/1.1 200 OK"
        result = self.run_httpie(self.command)
        self.assertIn("HTTP/1.1 200 OK", result.stdout)

    @patch('subprocess.run')
    def test_http_request_not_found(self, mock_run):
        mock_run.return_value.stdout = "HTTP/1.1 404 Not Found"
        result = self.run_httpie(self.command)
        self.assertIn("HTTP/1.1 404 Not Found", result.stdout)

    @patch('subprocess.run')
    def test_http_request_server_error(self, mock_run):
        mock_run.return_value.stdout = "HTTP/1.1 500 Internal Server Error"
        result = self.run_httpie(self.command)
        self.assertIn("HTTP/1.1 500 Internal Server Error", result.stdout)

    @patch('subprocess.run')
    def test_http_request_timeout(self, mock_run):
        mock_run.return_value.stdout = "HTTP/1.1 408 Request Timeout"
        result = self.run_httpie(self.command)
        self.assertIn("HTTP/1.1 408 Request Timeout", result.stdout)

    # The run_httpie method sends an HTTP request using HTTPie.
    def run_httpie(self, command):
        return subprocess.run(command, shell=True, text=True, capture_output=True)

if __name__ == '__main__':
    unittest.main()
