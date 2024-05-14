#!/bin/bash

cp -r ../functions/venv/lib/python3.11/site-packages/ python/

zip -r dependencies.zip python

rm -rf python/

output=$(aws lambda publish-layer-version \
  --layer-name crawler-service-dependencies \
  --zip-file fileb://dependencies.zip \
  --compatible-runtimes python3.10 python3.11 python3.12)

layer_arn=$(echo $output | jq -r '.LayerVersionArn')

aws lambda update-function-configuration \
  --function-name crawler-service-function \
  --layers $layer_arn

echo "Updated Lambda function 'crawler-service-function' with layer version: $layer_arn"
rm -f dependencies.zip