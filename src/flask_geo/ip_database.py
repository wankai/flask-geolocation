import os
from ipaddress import ip_address


def from_source(source: str):
    if source == "maxmind":
        return MaxmindDatabase()
    raise Exception("ip source not supported")


"""
class IPDatabase:
    def __init__(self):
        return None

    def load(self, path):
        return None

    return (country_code, country_symbol, country_name)
    all three elements in tuple is None if can't find
    country info for this IP

    def get(self, ip: str):
        return None
"""


class MaxmindDatabase:
    def __init__(self):
        self._addresses = {}
        self._codes = {}

    def load(self, path):
        self._path = path

        data_dir = _find_latest_database(self._path)

        code_file = _get_code_file(data_dir)
        self._load_country_code(code_file)

        ip_file = _get_ip_file(data_dir)
        self._load_ip_dict(ip_file)

    def _load_country_code(self, path):
        with open(path) as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                arr = line.strip().split(",")
                if len(arr) != 7:
                    continue
                if arr[0] == "geoname_id":
                    continue
                if not arr[4]:
                    continue

                self._codes[int(arr[0])] = (arr[4], arr[5].strip('"'))

    def __load_ip_items(self, path):
        items = []
        with open(path) as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                arr = line.strip().split(",")
                if len(arr) != 6:
                    continue
                if arr[0] == "network":
                    continue
                ip_arr = arr[0].split("/")
                if len(ip_arr) != 2:
                    continue
                if not arr[1]:
                    continue

                mask = int(ip_arr[1])
                address = int(ip_address(ip_arr[0]))
                code = int(arr[1])
                items.append((mask, address, code))

        return items

    def __get_grouped_items(self, items):
        grouped_items = []
        last_index = -1
        group_single = []
        for mask, address, code in items:
            if last_index > -1 and mask != items[last_index][0]:
                grouped_items.append(group_single.copy())
                group_single.clear()
            group_single.append((mask, address, code))
            last_index = last_index + 1

        if group_single:
            grouped_items.append(group_single)

        return grouped_items

    def _load_ip_dict(self, path):
        items = self.__load_ip_items(path)
        items.sort(key=lambda x: x[0])

        grouped_items = self.__get_grouped_items(items)

        for single in grouped_items:
            address_set = {}
            if single:
                mask = single[0][0]

            for _, address, code in single:
                if code in self._codes:
                    address_set[address] = self._codes[code]
            self._addresses[mask] = address_set

    def get(self, ip: str):
        ip_int = int(ip_address(ip))
        for mask_digit_num, address_map in self._addresses.items():
            mask = _mask_map[mask_digit_num]
            ip_after_mask = ip_int & mask
            if ip_after_mask in address_map:
                return address_map[ip_after_mask]


def _find_latest_database(path):
    all_dir1 = os.listdir(path)
    all_dir = map(lambda x: path + "/" + x, all_dir1)
    items = map(lambda x: (os.path.getmtime(x), x), all_dir)
    return max(items)[1]


def _get_code_file(path):
    return path + "/GeoLite2-Country-Locations-en.csv"


def _get_ip_file(path):
    return path + "/GeoLite2-Country-Blocks-IPv4.csv"


_mask_map = {
    31: 0xFFFFFFFE,
    30: 0xFFFFFFFC,
    29: 0xFFFFFFF8,
    28: 0xFFFFFFF0,
    27: 0xFFFFFFE0,
    26: 0xFFFFFFC0,
    25: 0xFFFFFF80,
    24: 0xFFFFFF00,
    23: 0xFFFFFE00,
    22: 0xFFFFFC00,
    21: 0xFFFFF800,
    20: 0xFFFFF000,
    19: 0xFFFFE000,
    18: 0xFFFFC000,
    17: 0xFFFF8000,
    16: 0xFFFF0000,
    15: 0xFFFE0000,
    14: 0xFFFC0000,
    13: 0xFFF80000,
    12: 0xFFF00000,
    11: 0xFFE00000,
    10: 0xFFC00000,
    9: 0xFF800000,
    8: 0xFF000000,
    7: 0xFE000000,
    6: 0xFC000000,
    5: 0xF8000000,
    4: 0xF0000000,
    3: 0xE0000000,
    2: 0xC0000000,
    1: 0x80000000,
    0: 0x00000000,
}
