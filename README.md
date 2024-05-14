# My Lambda Project

## Overview

This project contains two AWS Lambda functions:
1. **Website Crawler Function**: Crawls website data and uploads it to an S3 bucket.
2. **Database Importer Function**: Triggered by new files in the S3 bucket and imports data into MongoDB.

## Folder Structure

```
crawler-service-lambda/
├── terraform/
│   ├── main.tf
│   ├── s3.tf
│   ├── iam.tf
│   ├── lambda.tf
│   ├── variables.tf
│   ├── outputs.tf
├── functions/
│   ├── website-crawler/
│   │   ├── lambda_function.py
│   │   ├── requirements.txt
│   │   ├── venv/
│   ├── database-importer/
│   │   ├── lambda_function.py
│   │   ├── requirements.txt
│   │   ├── venv/
├── scripts/
│   ├── package_lambda.sh
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites

- Install Python 3.8+
- Install Terraform
- Install AWS CLI

### Setup Virtual Environments

1. Set up virtual environments for each function:

   ```bash
   cd functions/website-crawler
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   deactivate

   cd ../database-importer
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   deactivate
   ```

### Package Lambda Functions

Run the `package_lambda.sh` script to package the Lambda functions:

```bash
bash scripts/package_lambda.sh
```

### Deploy Infrastructure

1. Initialize Terraform:

   ```bash
   cd terraform
   terraform init
   ```

2. Apply the Terraform configuration:

   ```bash
   terraform apply
   ```

This will deploy the S3 bucket, Lambda functions, and other required resources to AWS.

## License

This project is licensed under the MIT License.
