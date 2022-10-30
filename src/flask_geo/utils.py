from flask import current_app
from flask import g
from flask import has_request_context
from werkzeug.local import LocalProxy

current_geo = LocalProxy(lambda: _get_geo())


def _get_geo():
    if has_request_context():
        if "_loaded_geo" not in g:
            current_app.geo_manager._load_geo()
        return g._loaded_geo
    return None


def _geo_context_processor():
    return dict(current_geo=_get_geo())
