#!/bin/bash

cd ../functions

ENVIRONMENT="${1:-local}"
ENV_FILE="environments/$ENVIRONMENT.json"
LAMBDA_FUNCTION_NAME="crawler-service-function"

if [ "$ENVIRONMENT" = "local" ]; then
    # Load environment variables from .env.json to local environment
    echo "Setting local environment variables from .env.json"
    ENV_VARS=$(cat $ENV_FILE | jq -r '.Variables | to_entries[] | .key + "=" + .value')
    echo $ENV_VARS
    export $(echo $ENV_VARS | xargs)
else
    # Read the environment variables from the JSON file
    ENV_VARS=$(cat $ENV_FILE)

    # Update the Lambda function environment variables
    aws lambda update-function-configuration \
      --function-name $LAMBDA_FUNCTION_NAME \
      --environment "$ENV_VARS"

    echo "Updated Lambda function '$LAMBDA_FUNCTION_NAME' with the new code package and environment variables."
fi
