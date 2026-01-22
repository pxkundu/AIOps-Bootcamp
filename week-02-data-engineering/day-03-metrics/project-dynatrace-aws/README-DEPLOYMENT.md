# Deployment Guide: AWS Metrics to Dynatrace

This guide walks you through deploying the AWS metrics collectors to forward CloudWatch metrics to Dynatrace.

---

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **Dynatrace Account** with API token
3. **AWS CLI** configured with credentials
4. **Python 3.9+** for local testing

---

## Step 1: Set Up IAM Role

Create an IAM role for Lambda functions with the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "ec2:DescribeInstances",
        "ec2:DescribeRegions",
        "lambda:ListFunctions",
        "lambda:GetFunction",
        "s3:ListBuckets",
        "s3:GetBucketLocation"
      ],
      "Resource": "*"
    }
  ]
}
```

**Create the role:**

```bash
aws iam create-role \
  --role-name lambda-cloudwatch-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam put-role-policy \
  --role-name lambda-cloudwatch-role \
  --policy-name CloudWatchMetricsPolicy \
  --policy-document file://iam-policy.json
```

---

## Step 2: Configure Dynatrace

1. **Get your Dynatrace environment URL:**
   - Format: `https://{your-environment-id}.live.dynatrace.com`
   - Or: `https://{your-domain}/e/{your-environment-id}`

2. **Create API Token:**
   - Go to **Dynatrace → Settings → Integration → Dynatrace API**
   - Create token with scope: `metrics.ingest`
   - Save the token securely

3. **Set environment variables:**
   ```bash
   export DYNATRACE_URL="https://your-environment.live.dynatrace.com"
   export DYNATRACE_API_TOKEN="your-api-token-here"
   ```

---

## Step 3: Deploy Collectors

### Option A: Using Deployment Script (Recommended)

```bash
chmod +x deploy.sh
./deploy.sh
```

### Option B: Manual Deployment

#### 3.1 Package Lambda Functions

```bash
# For each collector (lambda, s3, ec2)
cd collectors
zip -r ../lambda_collector.zip lambda_metrics_collector.py
pip install boto3 requests -t .
zip -r ../lambda_collector.zip . -x "*.pyc" -x "__pycache__/*"
```

#### 3.2 Create Lambda Function

```bash
aws lambda create-function \
  --function-name aws-metrics-to-dynatrace-lambda \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-cloudwatch-role \
  --handler index.lambda_handler \
  --zip-file fileb://lambda_collector.zip \
  --timeout 300 \
  --memory-size 512 \
  --environment Variables="{DYNATRACE_URL=${DYNATRACE_URL},DYNATRACE_API_TOKEN=${DYNATRACE_API_TOKEN}}"
```

#### 3.3 Create EventBridge Schedule

```bash
# Create rule
aws events put-rule \
  --name aws-metrics-to-dynatrace-lambda-schedule \
  --schedule-expression "rate(5 minutes)" \
  --state ENABLED

# Add Lambda as target
aws events put-targets \
  --rule aws-metrics-to-dynatrace-lambda-schedule \
  --targets "Id=1,Arn=arn:aws:lambda:REGION:ACCOUNT:function:aws-metrics-to-dynatrace-lambda"

# Grant permission
aws lambda add-permission \
  --function-name aws-metrics-to-dynatrace-lambda \
  --statement-id schedule-permission \
  --action 'lambda:InvokeFunction' \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:REGION:ACCOUNT:rule/aws-metrics-to-dynatrace-lambda-schedule
```

---

## Step 4: Verify Deployment

### 4.1 Test Lambda Function

```bash
# Invoke function manually
aws lambda invoke \
  --function-name aws-metrics-to-dynatrace-lambda \
  --payload '{}' \
  response.json

cat response.json
```

### 4.2 Check CloudWatch Logs

```bash
aws logs tail /aws/lambda/aws-metrics-to-dynatrace-lambda --follow
```

### 4.3 Verify Metrics in Dynatrace

1. Go to **Dynatrace → Metrics**
2. Search for: `aws.lambda.invocations`, `aws.s3.bucket_size`, `aws.ec2.cpu_utilization`
3. Verify metrics are appearing

---

## Step 5: Create Dashboards

### 5.1 Using Dynatrace UI

1. Go to **Dynatrace → Dashboards → Create Dashboard**
2. Add tiles for:
   - Lambda invocations and errors
   - S3 bucket size and requests
   - EC2 CPU and network

### 5.2 Using API

```bash
curl -X POST "${DYNATRACE_URL}/api/config/v1/dashboards" \
  -H "Authorization: Api-Token ${DYNATRACE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @dashboard.json
```

---

## Troubleshooting

### Metrics Not Appearing

1. **Check Lambda logs:**
   ```bash
   aws logs tail /aws/lambda/aws-metrics-to-dynatrace-lambda --follow
   ```

2. **Verify API token:**
   ```bash
   curl -X GET "${DYNATRACE_URL}/api/v2/metrics" \
     -H "Authorization: Api-Token ${DYNATRACE_API_TOKEN}"
   ```

3. **Check IAM permissions:**
   ```bash
   aws lambda get-policy --function-name aws-metrics-to-dynatrace-lambda
   ```

### High Costs

- Reduce collection frequency (change schedule to 15 minutes)
- Filter specific resources (modify collectors to skip certain buckets/instances)
- Use CloudWatch metric filters to reduce data volume

---

## Cost Estimation

**Lambda:**
- 3 functions × 5-minute schedule = 288 invocations/day
- ~100ms execution time = $0.20/month

**CloudWatch:**
- API calls: ~864 calls/day = $0.26/month
- Logs: ~1GB/month = $0.50/month

**Total: ~$1/month** for basic setup

---

## Next Steps

1. Set up alerts in Dynatrace for critical metrics
2. Create custom dashboards for your team
3. Integrate with Dynatrace AI for anomaly detection
4. Add custom metrics for your specific use cases

---

<p align="center">
  <a href="README.md">← Back to Project Overview</a>
</p>
