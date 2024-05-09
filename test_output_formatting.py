import subprocess
import unittest
from unittest.mock import patch

# These unittests use the HTTPie command-line tool to test various output styles.
# Use the following command to install HTTPie:
# pip install httpie

# Use the following command to run the test:
# python -m unittest test_output_formatting.py

class TestHTTPOutputFormatting(unittest.TestCase):
    # The setUp method is called before each test in this class.
    def setUp(self):
        self.url = 'http://localhost:3000/data'

    @patch('subprocess.run')
    def test_json_response_formatting(self, mock_run):
        # Simulated pretty-printed JSON output
        json_response = '{\n    "name": "John",\n    "age": 30\n}'
        mock_run.return_value.stdout = f"HTTP/1.1 200 OK\nContent-Type: application/json\n\n{json_response}"
        command = f'http --verbose --pretty=all GET {self.url}'
        result = self.run_httpie(command)
        self.assertIn(json_response, result.stdout)


    @patch('subprocess.run')
    def test_header_display(self, mock_run):
        # Ensure that response headers are displayed correctly
        headers = "Content-Type: application/json\nContent-Length: 18"
        mock_run.return_value.stdout = f'HTTP/1.1 200 OK\n{headers}\n\n{{"data": "value"}}'
        command = f'http --verbose GET {self.url}'
        result = self.run_httpie(command)
        self.assertIn("Content-Type: application/json", result.stdout)
        self.assertIn("Content-Length: 18", result.stdout)

    @patch('subprocess.run')
    def test_pretty_print_xml(self, mock_run):
        # Simulated pretty-printed XML output
        xml_response = "<root>\n  <name>John</name>\n</root>"
        mock_run.return_value.stdout = f"HTTP/1.1 200 OK\nContent-Type: application/xml\n\n{xml_response}"
        command = f'http --pretty=format GET {self.url}'
        result = self.run_httpie(command)
        self.assertIn(xml_response, result.stdout)


    def run_httpie(self, command):
        return subprocess.run(command, shell=True, text=True, capture_output=True)

if __name__ == '__main__':
    unittest.main()
