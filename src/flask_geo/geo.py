from dataclasses import dataclass


@dataclass
class Geo:
    ip: str
    country_symbol: str
    country_name: str
    timezone: str

    def is_china(self):
        return self.country_symbol == "CN"

    def is_usa(self):
        return self.country_symbol == "US"
