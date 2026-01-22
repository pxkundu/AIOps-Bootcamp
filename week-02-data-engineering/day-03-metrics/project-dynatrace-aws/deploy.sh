#!/bin/bash
# Deployment script for AWS Metrics Collectors to Dynatrace

set -e

# Configuration
FUNCTION_NAME_PREFIX="aws-metrics-to-dynatrace"
RUNTIME="python3.9"
TIMEOUT=300
MEMORY_SIZE=512
SCHEDULE_RATE="5 minutes"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Deploying AWS Metrics Collectors to Dynatrace${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if environment variables are set
if [ -z "$DYNATRACE_URL" ] || [ -z "$DYNATRACE_API_TOKEN" ]; then
    echo -e "${YELLOW}Warning: DYNATRACE_URL or DYNATRACE_API_TOKEN not set${NC}"
    echo "Please set these environment variables:"
    echo "  export DYNATRACE_URL=https://your-environment.live.dynatrace.com"
    echo "  export DYNATRACE_API_TOKEN=your-api-token"
    exit 1
fi

# Create deployment package
echo "Creating deployment packages..."
for collector in lambda s3 ec2; do
    echo "  Packaging ${collector} collector..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cp collectors/${collector}_metrics_collector.py ${TEMP_DIR}/index.py
    
    # Install dependencies
    cd ${TEMP_DIR}
    pip install boto3 requests -t . --quiet
    cd -
    
    # Create zip file
    zip -r ${collector}_collector.zip ${TEMP_DIR}/* -q
    
    # Cleanup
    rm -rf ${TEMP_DIR}
done

# Deploy Lambda functions
echo "Deploying Lambda functions..."

for collector in lambda s3 ec2; do
    FUNCTION_NAME="${FUNCTION_NAME_PREFIX}-${collector}"
    
    echo "  Deploying ${FUNCTION_NAME}..."
    
    # Check if function exists
    if aws lambda get-function --function-name ${FUNCTION_NAME} &> /dev/null; then
        echo "    Updating existing function..."
        aws lambda update-function-code \
            --function-name ${FUNCTION_NAME} \
            --zip-file fileb://${collector}_collector.zip \
            --quiet
        
        # Update environment variables
        aws lambda update-function-configuration \
            --function-name ${FUNCTION_NAME} \
            --environment Variables="{DYNATRACE_URL=${DYNATRACE_URL},DYNATRACE_API_TOKEN=${DYNATRACE_API_TOKEN}}" \
            --timeout ${TIMEOUT} \
            --memory-size ${MEMORY_SIZE} \
            --quiet
    else
        echo "    Creating new function..."
        
        # Create IAM role (simplified - you should create a proper role)
        ROLE_ARN=$(aws iam get-role --role-name lambda-cloudwatch-role --query 'Role.Arn' --output text 2>/dev/null || echo "")
        
        if [ -z "$ROLE_ARN" ]; then
            echo -e "${YELLOW}    Warning: IAM role 'lambda-cloudwatch-role' not found${NC}"
            echo "    Please create an IAM role with CloudWatch read permissions"
            exit 1
        fi
        
        aws lambda create-function \
            --function-name ${FUNCTION_NAME} \
            --runtime ${RUNTIME} \
            --role ${ROLE_ARN} \
            --handler index.lambda_handler \
            --zip-file fileb://${collector}_collector.zip \
            --timeout ${TIMEOUT} \
            --memory-size ${MEMORY_SIZE} \
            --environment Variables="{DYNATRACE_URL=${DYNATRACE_URL},DYNATRACE_API_TOKEN=${DYNATRACE_API_TOKEN}}" \
            --quiet
    fi
    
    # Create or update EventBridge rule for scheduling
    RULE_NAME="${FUNCTION_NAME}-schedule"
    
    if aws events describe-rule --name ${RULE_NAME} &> /dev/null; then
        echo "    Updating schedule rule..."
        aws events put-rule \
            --name ${RULE_NAME} \
            --schedule-expression "rate(${SCHEDULE_RATE})" \
            --quiet
    else
        echo "    Creating schedule rule..."
        aws events put-rule \
            --name ${RULE_NAME} \
            --schedule-expression "rate(${SCHEDULE_RATE})" \
            --state ENABLED \
            --quiet
        
        # Add permission for EventBridge to invoke Lambda
        aws lambda add-permission \
            --function-name ${FUNCTION_NAME} \
            --statement-id ${RULE_NAME}-permission \
            --action 'lambda:InvokeFunction' \
            --principal events.amazonaws.com \
            --source-arn $(aws events describe-rule --name ${RULE_NAME} --query 'Arn' --output text) \
            --quiet
    fi
    
    # Add Lambda as target
    FUNCTION_ARN=$(aws lambda get-function --function-name ${FUNCTION_NAME} --query 'Configuration.FunctionArn' --output text)
    
    aws events put-targets \
        --rule ${RULE_NAME} \
        --targets "Id=1,Arn=${FUNCTION_ARN}" \
        --quiet
    
    echo -e "    ${GREEN}✓ ${FUNCTION_NAME} deployed successfully${NC}"
done

# Cleanup
echo "Cleaning up..."
rm -f *_collector.zip

echo -e "${GREEN}Deployment complete!${NC}"
echo ""
echo "Functions deployed:"
echo "  - ${FUNCTION_NAME_PREFIX}-lambda"
echo "  - ${FUNCTION_NAME_PREFIX}-s3"
echo "  - ${FUNCTION_NAME_PREFIX}-ec2"
echo ""
echo "Metrics will be collected every ${SCHEDULE_RATE}"
