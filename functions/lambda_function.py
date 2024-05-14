import csv
import pprint
from crawler import get_post_urls, get_post_details
from rental_service import RentalService
import boto3
import json
from datetime import datetime
import os


s3 = boto3.client("s3")


def lambda_handler(event, context):
    crawl_urls = os.getenv("CRAWLING_URLS").split("@")
    rental_service = RentalService()
    is_s3_upload = False

    data = []
    for object in crawl_urls:
        url = object.split(",")[0]
        property_type = object.split(",")[1]
        transaction_type = object.split(",")[2]

        post_urls = get_post_urls(url)

        for post_url in post_urls:
            callback = lambda post: rental_service.store_post(post)
            post_details = get_post_details(post_url, property_type, transaction_type, callback)
            data.append(post_details)

    # Create a CSV file
    if is_s3_upload:
        csv_file = "/tmp/data.csv"

        if len(data) == 0:
            return {
                "statusCode": 200,
                "body": json.dumps("No data to write to CSV file!"),
            }

        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data[0].keys())  # Write headers
            writer.writerows(map(lambda data: data.values(), data))

        bucket_name = os.getenv("S3_BUCKET_NAME")
        s3_file_name = f'mogi-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'

        s3.upload_file(csv_file, bucket_name, s3_file_name)

    return {
        "statusCode": 200,
        "body": json.dumps("CSV file created and uploaded to S3 successfully!"),
    }


print(os.getenv("ENVIRONMENT"))
if os.getenv("ENVIRONMENT") == "local":
    lambda_handler(None, None)
