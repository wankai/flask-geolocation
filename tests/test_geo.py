import sys
import unittest

from flask import Flask

from semantic_version import Version

from flask_geo import GeoManager
from flask_geo.__about__ import __title__
from flask_geo.__about__ import __description__
from flask_geo.__about__ import __url__
from flask_geo.__about__ import __version_info__
from flask_geo.__about__ import __version__
from flask_geo.__about__ import __author__
from flask_geo.__about__ import __author_email__
from flask_geo.__about__ import __maintainer__
from flask_geo.__about__ import __license__
from flask_geo.__about__ import __copyright__

sys_version = Version(
    major=sys.version_info.major,
    minor=sys.version_info.minor,
    patch=sys.version_info.micro,
)


class AboutTestCase(unittest.TestCase):
    """make sure we can get version and other info."""
    def test_have_about_data(self):
        self.assertTrue(__title__ is not None)
        self.assertTrue(__description__ is not None)
        self.assertTrue(__url__ is not None)
        self.assertTrue(__version_info__ is not None)
        self.assertTrue(__version__ is not None)
        self.assertTrue(__author__ is not None)
        self.assertTrue(__author_email__ is not None)
        self.assertTrue(__maintainer__ is not None)
        self.assertTrue(__license__ is not None)
        self.assertTrue(__copyright__ is not None)


class InitializationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "1234"

    def test_init_app(self):
        geo_manager = GeoManager()
        geo_manager.init_app(self.app, add_context_processor=True)
        self.assertIsInstance(geo_manager, GeoManager)
