# Flask-Geolocation
Flask-Geolocation aims to help get geolocation informaton for Flask app

# Installation
pip install flask-geolocation

# Usage

```python
from flask-geolocation import GeoManager

geo_manager = GeoManager()
geo_manager.init_app(app)
```

```python
current_geo.ip
current_geo.country_symbol
current_geo.country_name
current_geo.timezone
```
