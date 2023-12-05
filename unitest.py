import requests
import unittest
url = "http://127.0.0.1:5000"

class TestSiteAvialble(unittest.TestCase):

    def url_test(self):
        try:
            response = requests.head(url).status_code
        except requests.ConnectionError as e:
            response = e
        self.assertEqual(response, 200, "site not reachable")


if __name__ == '__main__':
    unittest.main()
