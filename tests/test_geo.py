import sys
import unittest

from flask import Flask
from flask_geo import current_geo
from flask_geo import GeoManager
from flask_geo.__about__ import __author__
from flask_geo.__about__ import __author_email__
from flask_geo.__about__ import __copyright__
from flask_geo.__about__ import __description__
from flask_geo.__about__ import __license__
from flask_geo.__about__ import __maintainer__
from flask_geo.__about__ import __title__
from flask_geo.__about__ import __url__
from flask_geo.__about__ import __version__
from flask_geo.__about__ import __version_info__
from semantic_version import Version

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

    def test_class_init(self):
        geo_manager = GeoManager(self.app, add_context_processor=True)
        self.assertIsInstance(geo_manager, GeoManager)


class IpTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "1234"

        self.geo_manager = GeoManager()
        self.geo_manager.init_app(self.app)

        @self.app.route("/")
        def index():
            return current_geo.country_symbol

    def test_ip_with_request(self):
        with self.app.test_client() as c:
            result = c.get("/", environ_base={"REMOTE_ADDR": "154.204.60.219"})
            self.assertEqual("HK", result.data.decode("utf-8"))
