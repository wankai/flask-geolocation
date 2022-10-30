import re

IP_DATABASE_SOURCE = "maxmind"
IP_DATABASE_PATH = "data"

MAXMIND_DIR_PATTERN = re.compile(r"GeoLite2-Country-CSV_\d{6}")
