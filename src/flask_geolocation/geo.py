from dataclasses import dataclass


@dataclass
class Geo:
    ip: str
    country_symbol: str
    country_name: str
    timezone: str
