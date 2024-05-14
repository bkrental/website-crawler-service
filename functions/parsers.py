import re


def parse_price(price_str):
    price_regex = r"((\d+)tỷ)?((\d+)triệu)?((\d+)nghìn)?"
    x = re.search(price_regex, price_str.replace(" ", ""))

    if x is not None:
        thousand = int(x.group(6)) if x.group(6) else 0
        million = int(x.group(4)) if x.group(4) else 0
        billion = int(x.group(2)) if x.group(2) else 0

        return thousand * pow(10, -3) + million + billion * pow(10, 3)

    return 0


def parse_phone_number(owner_contact):
    contact_regex = r"PhoneFormat\('(\d+)'\)"
    x = re.search(contact_regex, owner_contact)

    if x is not None:
        return x.group(1)

    return None


def parse_address(address):
    address_details = address.strip().split(", ")

    district_pattern = r"(Quận (2|9|Thủ Đức))( \(TP\.? Thủ Đức\))?"
    province = address_details[-1]
    district = address_details[-2]

    if re.match(district_pattern, address_details[-2]):
        province = "TP. Thủ Đức"
        district = re.search(district_pattern, address_details[-2]).group(1)

    return {
        "province": province,
        "district": district,
        "ward": address_details[-3],
        "street": address_details[-4],
    }


def parse_area(area):
    area_regex = r"(\d+) m"
    x = re.search(area_regex, area)

    if x is not None:
        return int(x.group(1))

    return None
