import requests
from bs4 import BeautifulSoup
from parsers import parse_address, parse_area, parse_phone_number, parse_price


def get_html_content(url: str) -> str:
    res = requests.get(url)
    if res.status_code != 200:
        print(f"[ERROR] Failed to fetch {url}")
        return ""

    return res.text


def get_post_urls(url):
    html_content = get_html_content(url)
    soup = BeautifulSoup(html_content, "html.parser")

    posts = soup.select("ul.props > *")
    return [post.select_one("a.link-overlay").get("href", None) for post in posts]


def get_post_details(post_details_url: str, property_type, transasction_type, callback) -> dict:
    html_content = get_html_content(post_details_url)
    soup = BeautifulSoup(html_content, "html.parser")

    post_details = {}
    post_details["name"] = soup.select_one(".title > h1").text.strip()
    post_details["displayed_address"] = soup.select_one(".address").text.strip()
    post_details["address"] = parse_address(soup.select_one(".address").text.strip())
    post_details["price"] = parse_price(soup.select_one("div.price").text.strip())
    post_details["description"] = " ".join(
        soup.select_one(".info-content-body").strings
    )
    post_details["property_type"] = property_type
    post_details["transaction_type"] = transasction_type

    post_details["thumbnail"] = soup.select_one(".media-item img")["src"]
    post_details["images"] = [
        img["data-src"] for img in soup.select(".media-item img")[1:]
    ]

    google_map_link = soup.select_one('iframe[title="map"]')["data-src"]
    lat, lon = google_map_link.split("q=")[1].split(",")

    post_details["location"] = {
        "type": "Point",
        "coordinates": [float(lon), float(lat)],
    }
    optional_properties = soup.select("div.info-attrs.clearfix > div")
    for prop in optional_properties:
        prop_name = prop.select_one("span:nth-of-type(1)").text
        prop_value = prop.select_one("span:nth-of-type(2)").text

        if "Diện tích sử dụng" in prop_name:
            post_details["area"] = parse_area(prop_value)
        elif "Phòng ngủ" in prop_name:
            post_details["bedrooms"] = int(prop_value) if prop_value.isdigit() else prop_value
        elif "Nhà tắm" in prop_name:
            post_details["bathrooms"] = int(prop_value) if prop_value.isdigit() else prop_value
        # elif "Ngày đăng" in prop_name:
        #     post_details["published_date"] = prop_value

    # post_details["owner_name"] = soup.select_one(".agent-info img")["alt"]
    # post_details["owner_contact"] = parse_phone_number(soup.select_one(".agent-contact a:first-child span")["ng-bind"])
    post_details["contact"] = {
        "name": soup.select_one(".agent-info img")["alt"],
        "phone": parse_phone_number(soup.select_one(".agent-contact a:first-child span")["ng-bind"]),
    }
    post_details["post_url"] = post_details_url
    post_details["source"] = "mogi.vn"

    if callback:
        callback(post_details)

    return post_details
