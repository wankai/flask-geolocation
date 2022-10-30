import unittest

from ip_database import from_source
from ip_database import MaxmindDatabase
from config import IP_DATABASE_SOURCE

class TestMaxmindDatabase(unittest.TestCase):
    def setUp(self):
        self.db = from_source(IP_DATABASE_SOURCE)
        self.db.load("/home/lighthouse/macro_watch/offline/maxmind/data")

    def test_china(self):
        info = self.db.get("121.34.22.206")
        self.assertEqual(info, ("CN", "China"))
    def test_sigapore(self):
        info = self.db.get("43.156.97.49")
        self.assertEqual(info, ("SG", "Singapore"))
    def test_hongkong(self):
        info = self.db.get("154.204.60.219")
        self.assertEqual(info, ("HK", "Hong Kong"))

if __name__ == '__main__':
    unittest.main()
