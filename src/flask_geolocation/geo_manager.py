from flask import g
from flask import request

from . import ip_database
from .geo import Geo
from .timezone import timezone_map
from .utils import _geo_context_processor


class GeoManager:
    def __init__(self, ip_data_path=None):
        self.ip_data_path = ip_data_path
        if self.ip_data_path is None:
            self.ip_data_path = "maxmind/data"

        self.ip_data_source = "maxmind"
        self.ip_db = None

        self._ip_callback = None
        self._timezone_callback = None

    def init_app(self, app, add_context_processor=True):
        if self.ip_db is None:
            self.ip_db = ip_database.from_source(self.ip_data_source)
            self.ip_db.load(self.ip_data_path)

        app.geo_manager = self
        if add_context_processor:
            app.context_processor(_geo_context_processor)

    def use_ip(self, callback):
        """get ip for current user, all other infos rely on ip"""
        self._ip_callback = callback
        return self._ip_callback

    @property
    def ip_callback(self):
        return self._ip_callback

    def use_timezone(self, callback):
        self._timezone_callback = callback
        return self.timezone_callback

    @property
    def timezone_callback(self):
        return self._timezone_callback

    def _load_geo(self):
        """construct geo info from ip address"""
        ip = None
        if self._ip_callback is not None:
            ip = self._ip_callback()
        else:
            if request.headers.getlist("X-Forwarded-For"):
                ip = request.headers.getlist("X-Forwarded-For")[0]
            else:
                ip = request.remote_addr

        (country_symbol, country_name) = self.ip_db.get(ip)

        timezone = timezone_map[country_symbol]
        if self._timezone_callback:
            tz = self._timezone_callback()
            if tz is not None:
                timezone = tz

        geo = Geo(
            ip=ip,
            country_symbol=country_symbol,
            country_name=country_name,
            timezone=timezone,
        )
        g._loaded_geo = geo
