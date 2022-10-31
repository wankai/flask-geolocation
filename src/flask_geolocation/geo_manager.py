from flask import g
from flask import request

from . import ip_database
from .config import IP_DATABASE_PATH
from .config import IP_DATABASE_SOURCE
from .geo import Geo
from .timezone import timezone_map
from .utils import _geo_context_processor


class GeoManager:
    def __init__(self, ipdb=None, app=None, add_context_processor=True):
        self._ip_callback = None
        self._timezone_callback = None
        if ipdb is None:
            self.ipdb = ip_database.from_source(IP_DATABASE_SOURCE)
            self.ipdb.load(IP_DATABASE_PATH)
        else:
            self.ipdb = ipdb

        if app is not None:
            self.init_app(app, add_context_processor)

    def init_app(self, app, add_context_processor=True):
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

        (country_symbol, country_name) = self.ipdb.get(ip)

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
