import unittest

from flask_geo import config
from flask_geo import ip_database


class TestMaxmindDatabase(unittest.TestCase):
    def setUp(self):
        self.db = ip_database.from_source(config.IP_DATABASE_SOURCE)
        self.db.load("data")

    def test_china(self):
        info = self.db.get("121.34.22.206")
        self.assertEqual(info, ("CN", "China"))

    def test_sigapore(self):
        info = self.db.get("43.156.97.49")
        self.assertEqual(info, ("SG", "Singapore"))

    def test_hongkong(self):
        info = self.db.get("154.204.60.219")
        self.assertEqual(info, ("HK", "Hong Kong"))
