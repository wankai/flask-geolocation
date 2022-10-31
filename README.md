# Flask-Geolocation
Flask-Geolocation aims to help get geolocation informaton for Flask app

# Installation
install the extension with pip
```python
pip install flask-geolocation
```

# Usage
initialization
```python
from flask-geolocation import GeoManager

geo_manager = GeoManager()
geo_manager.init_app(app)
```

get geolocation related info with flask global variable current_geo
```python
from flask-geolocation import current_geo

current_geo.ip
current_geo.country_symbol
current_geo.country_name
current_geo.timezone
```

you can also use current_geo in template
```html
<html en="lang">
  <head>
  </head>
  <body>
    <p>ip: {{current_geo.ip}}</p>
    <p>country_symbol: {{current_geo.country_symbol}}</p>
    <p>country_name: {{current_geo.country_name}}</p>
    <p>timezone: {{current_geo.timezone}}</p>
  </body>
</html>
```
