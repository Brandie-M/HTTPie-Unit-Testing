import subprocess
import unittest

# These unittests use the HTTPie command-line tool to send HTTP requests to a server.
# Use the following command to install HTTPie:
# pip install httpie

# Use the following command to run the test:
# python -m unittest test_url_formatting.py

class TestHTTPieURLFormatting(unittest.TestCase):
    def run_httpie(self, url):
        command = f'http --offline --verbose GET {url}'
        return subprocess.run(command, shell=True, text=True, capture_output=True)

    def test_standard_url(self):
        """Test standard URL processing."""
        result = self.run_httpie('http://localhost:3000')
        self.assertIn("Host: localhost:3000", result.stdout)

    def test_url_with_path(self):
        """Test URL processing with path."""
        result = self.run_httpie('http://localhost:3000/api/data')
        self.assertIn("GET /api/data HTTP/1.1", result.stdout)

    def test_url_with_query(self):
        """Test URL processing with query parameters."""
        result = self.run_httpie('http://localhost:3000/search?q=hello')
        self.assertIn("GET /search?q=hello HTTP/1.1", result.stdout)

    def test_https_url(self):
        """Test HTTPS URL processing."""
        result = self.run_httpie('https://localhost')
        self.assertIn("Host: localhost", result.stdout)

    def test_url_with_special_characters(self):
        """Test URL with special characters in path."""
        result = self.run_httpie("http://localhost:3000/special%20chars")
        self.assertIn("GET /special%20chars HTTP/1.1", result.stdout)

    def test_url_with_port(self):
        """Test URL with explicit port."""
        result = self.run_httpie('http://localhost:8080')
        self.assertIn("Host: localhost:8080", result.stdout)

    def test_ip_address_url(self):
        """Test URL with IP address."""
        result = self.run_httpie('http://192.168.1.1')
        self.assertIn("Host: 192.168.1.1", result.stdout)

if __name__ == '__main__':
    unittest.main()
