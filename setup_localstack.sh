#!/bin/bash
set -e

REGION="sa-east-1"
export AWS_DEFAULT_REGION=$REGION

echo "🏗️  Registrando função Lambda..."

IMAGE_NAME="scraper-lambda"

# Cria a função Lambda baseada em imagem local
awslocal lambda create-function \
  --function-name scraper-imoveis \
  --package-type Image \
  --code ImageUri=$IMAGE_NAME \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --region $REGION

echo "🌐 Criando API Gateway REST para a Lambda..."

API_ID=$(awslocal apigateway create-rest-api --name "scraper-api" --region $REGION | jq -r .id)
PARENT_ID=$(awslocal apigateway get-resources --rest-api-id "$API_ID" --region $REGION | jq -r '.items[0].id')

# Cria o recurso /health
RESOURCE_ID=$(awslocal apigateway create-resource \
  --rest-api-id "$API_ID" \
  --parent-id "$PARENT_ID" \
  --path-part "health" \
  --region $REGION | jq -r .id)

# Configura o método GET
awslocal apigateway put-method \
  --rest-api-id "$API_ID" \
  --resource-id "$RESOURCE_ID" \
  --http-method GET \
  --authorization-type "NONE" \
  --region $REGION

# Vincula o método à Lambda
awslocal apigateway put-integration \
  --rest-api-id "$API_ID" \
  --resource-id "$RESOURCE_ID" \
  --http-method GET \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/arn:aws:lambda:$REGION:000000000000:function:scraper-imoveis/invocations \
  --region $REGION

# Permite que o API Gateway invoque a Lambda
awslocal lambda add-permission \
  --function-name scraper-imoveis \
  --statement-id apigw-test \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn arn:aws:execute-api:$REGION:000000000000:$API_ID/*/GET/health \
  --region $REGION

# Realiza o deploy da API
awslocal apigateway create-deployment \
  --rest-api-id "$API_ID" \
  --stage-name dev \
  --region $REGION

echo "✅ API pronta em: http://localhost:4566/restapis/$API_ID/dev/_user_request_/health"
