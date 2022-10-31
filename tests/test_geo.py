import os
import sys
import unittest

from flask import Flask
from flask import render_template
from flask_geolocation import current_geo
from flask_geolocation import GeoManager
from flask_geolocation.__about__ import __author__
from flask_geolocation.__about__ import __author_email__
from flask_geolocation.__about__ import __copyright__
from flask_geolocation.__about__ import __description__
from flask_geolocation.__about__ import __license__
from flask_geolocation.__about__ import __maintainer__
from flask_geolocation.__about__ import __title__
from flask_geolocation.__about__ import __url__
from flask_geolocation.__about__ import __version__
from flask_geolocation.__about__ import __version_info__
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
        geo_manager = GeoManager("wrong_path")
        self.assertIsInstance(geo_manager, GeoManager)

    def test_init_with_ip_data_path(self):
        geo_manager = GeoManager("tests/data")
        geo_manager.init_app(self.app, add_context_processor=True)
        self.assertIsInstance(geo_manager, GeoManager)


class NoCallbackTestCase(unittest.TestCase):
    def setUp(self):
        template_abs = os.path.abspath("tests/templates")
        self.app = Flask(__name__, template_folder=template_abs)
        self.app.config["SECRET_KEY"] = "1234"

        self.environ_base = {"REMOTE_ADDR": "154.204.60.219"}

        self.geo_manager = GeoManager("tests/data")

        self.geo_manager.init_app(self.app)

        @self.app.route("/")
        def index():
            return (
                current_geo.country_symbol
                + ", "
                + current_geo.country_name
                + ", "
                + current_geo.timezone
            )

        @self.app.route("/template")
        def template():
            return render_template("country.html")

    def test_global_with_request(self):
        with self.app.test_client() as c:
            result = c.get("/", environ_base=self.environ_base)
            expect = "HK, Hong Kong, UTC+8"
            self.assertEqual(expect, result.data.decode("utf-8"))

    def test_template_context_with_request(self):
        with self.app.test_client() as c:
            result = c.get("/template", environ_base=self.environ_base)
            expect = "HK, Hong Kong, UTC+8"
            self.assertEqual(expect, result.data.decode("utf-8"))


class IpCallbackTestCase(unittest.TestCase):
    def setUp(self):
        template_abs = os.path.abspath("tests/templates")
        self.app = Flask(__name__, template_folder=template_abs)
        self.app.config["SECRET_KEY"] = "1234"

        self.environ_base = {"REMOTE_ADDR": "154.204.60.219"}

        self.geo_manager = GeoManager("tests/data")
        self.geo_manager.init_app(self.app)

        @self.geo_manager.use_ip
        def ip_callback():
            """This is a ip address in Singapore"""
            return "43.156.97.49"

        @self.app.route("/")
        def index():
            return (
                current_geo.country_symbol
                + ", "
                + current_geo.country_name
                + ", "
                + current_geo.timezone
            )

        @self.app.route("/template")
        def template():
            return render_template("country.html")

    def test_global_with_request(self):
        with self.app.test_client() as c:
            result = c.get("/", environ_base=self.environ_base)
            expect = "SG, Singapore, UTC+8"
            self.assertEqual(expect, result.data.decode("utf-8"))

    def test_template_context_with_request(self):
        with self.app.test_client() as c:
            result = c.get("/template", environ_base=self.environ_base)
            expect = "SG, Singapore, UTC+8"
            self.assertEqual(expect, result.data.decode("utf-8"))


class TimezoneCallbackTestCase(unittest.TestCase):
    def setUp(self):
        template_abs = os.path.abspath("tests/templates")
        self.app = Flask(__name__, template_folder=template_abs)
        self.app.config["SECRET_KEY"] = "1234"

        self.environ_base = {"REMOTE_ADDR": "154.204.60.219"}

        self.geo_manager = GeoManager("tests/data")
        self.geo_manager.init_app(self.app)

        @self.geo_manager.use_timezone
        def timezone_callback():
            """change Hong Kong timezone to UTC-4"""
            return "UTC-4"

        @self.app.route("/")
        def index():
            return (
                current_geo.country_symbol
                + ", "
                + current_geo.country_name
                + ", "
                + current_geo.timezone
            )

        @self.app.route("/template")
        def template():
            return render_template("country.html")

    def test_global_with_request(self):
        with self.app.test_client() as c:
            result = c.get("/", environ_base=self.environ_base)
            expect = "HK, Hong Kong, UTC-4"
            self.assertEqual(expect, result.data.decode("utf-8"))

    def test_template_context_with_request(self):
        with self.app.test_client() as c:
            result = c.get("/template", environ_base=self.environ_base)
            expect = "HK, Hong Kong, UTC-4"
            self.assertEqual(expect, result.data.decode("utf-8"))
