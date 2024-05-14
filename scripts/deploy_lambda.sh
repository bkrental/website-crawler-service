#!/bin/bash

cd ../functions

LAMBDA_FUNCTION_NAME=crawler-service-function
ZIP_FILE_NAME=source-code.zip

rm -f $ZIP_FILE_NAME

zip -r $ZIP_FILE_NAME *.py

aws lambda update-function-code \
  --function-name $LAMBDA_FUNCTION_NAME \
  --zip-file fileb://$ZIP_FILE_NAME

echo "Updated Lambda function '$LAMBDA_FUNCTION_NAME' with the new code package."

rm -f $ZIP_FILE_NAME
