import os
import requests

RENTAL_SERVICE_URL = os.getenv("RENTAL_SERVICE_URL")


class RentalService:
    def __init__(self):
        # Login to the rental service
        self.RENTAL_SERVICE_URL = os.getenv("RENTAL_SERVICE_URL")

        res = requests.post(
            f"{self.RENTAL_SERVICE_URL}/auth/login",
            json={"phone": "mogi_crawler", "password": "password123"},
        )

        if res.status_code != 200:
            raise Exception("Failed to login to the rental service")

        self.access_token = res.json()["data"]["access_token"]

    def store_post(self, post):
        res = requests.post(
            f"{self.RENTAL_SERVICE_URL}/posts",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json=post,
        )

        if res.status_code != 201:
            print(f"ERROR: Failed to store posts {post['name']}")
            print(res.json()["message"])
