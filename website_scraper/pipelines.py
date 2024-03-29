import re
import requests
from itemadapter import ItemAdapter


class MogiPipeline:
    def __init__(self):
        # Login to the rental service
        res = requests.post(
            "http://localhost:3000/auth/login",
            json={"phone": "mogi_crawler", "password": "password123"},
        )

        if res.status_code != 200:
            raise Exception("Failed to login to the rental service")

        self.access_token = res.json()["data"]["access_token"]

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Store to database
        res = requests.post(
            "http://localhost:3000/posts",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json={
                "name": adapter["title"],
                "description": adapter["description"],
                "property_type": "room",
                "transaction_type": "rent",
                "price": float(self.parse_price(adapter["price"])),
                "address": self.parse_address(adapter["address"]),
                "location": {
                    "type": "Point",
                    "coordinates": adapter["coordinates"],
                },
                "thumbnail": adapter["thumbnail"],
                "images": adapter["images"],
                "contact": {
                    "name": adapter["owner_name"],
                    "phone": self.parse_phone_number(adapter["owner_contact"]),
                },
                "post_url": adapter["post_url"],
                "source": "mogi.vn",
                "area": self.parse_area(adapter["area"]),
                "bedrooms": adapter["bedrooms"],
                "bathrooms": adapter["bathrooms"],
            },
        )

        if res.status_code != 201:
            print(res.json())
            raise Exception(
                f"Failed to store post to the rental service. Status code: {res.status_code}"
            )

        return item

    def parse_price(self, price_str):
        price_regex = r"((\d+)tỷ)?((\d+)triệu)?((\d+)nghìn)?"
        x = re.search(price_regex, price_str.replace(" ", ""))

        if x is not None:
            thousand = int(x.group(6)) if x.group(6) else 0
            million = int(x.group(4)) if x.group(4) else 0
            billion = int(x.group(2)) if x.group(2) else 0

            return thousand * pow(10, -3) + million + billion * pow(10, 3)

        return 0

    def parse_phone_number(self, owner_contact):
        contact_regex = r"PhoneFormat\('(\d+)'\)"
        x = re.search(contact_regex, owner_contact)

        if x is not None:
            return x.group(1)

        return None

    def parse_address(self, address):
        address_details = address.strip().split(", ")

        return {
            "province": address_details[-1],
            "district": address_details[-2],
            "ward": address_details[-3],
            "street": address_details[-4],
        }

    def parse_area(self, area):
        area_regex = r"(\d+) m"
        x = re.search(area_regex, area)

        if x is not None:
            return int(x.group(1))

        return None
