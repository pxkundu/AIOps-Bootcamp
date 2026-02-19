# AWS Setup Guide: Datadog Integration (Real-World)

To implement **The Noise Canceller** project, follow these steps to link your AWS environment to Datadog.

---

## 🔐 1. IAM Policy (The Least Privilege Way)

Create an IAM Policy named `DatadogIntegrationPolicy` with the following permissions. This allows Datadog to collect metrics and tags without giving it full access.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "apigateway:GET",
                "autoscaling:Describe*",
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*",
                "ec2:Describe*",
                "ec2:Get*",
                "rds:Describe*",
                "rds:List*",
                "tag:GetResources",
                "tag:GetTagKeys",
                "tag:GetTagValues"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```

## 🏗️ 2. AWS Role Setup

1.  Go to the **IAM Console** -> **Roles** -> **Create Role**.
2.  Select **Another AWS Account**.
3.  **Account ID:** `464622532012` (This is Datadog's production account ID).
4.  **External ID:** Copy this from your [Datadog AWS Integration Page](https://app.datadoghq.com/account/settings#integrations/amazon_web_services).
5.  Attach the `DatadogIntegrationPolicy` created in Step 1.

---

## 📡 3. Metric Streams (Fast Delivery)

For Intelligent Alerting, you need metrics faster than the standard 5-minute CloudWatch polling.
1.  In AWS, go to **CloudWatch** -> **Metrics** -> **Streams**.
2.  Click **Create metric stream**.
3.  Choose **Datadog** as the provider.
4.  AWS will provide a CloudFormation template to setup a Kinesis Firehose that pushes metrics to Datadog in real-time.

---

## 🖥️ 4. Deploying the Test "Victim" (EC2)

To see anomalies, we need an instance running the Datadog Agent. Use this **User Data** script when launching an EC2:

```bash
#!/bin/bash
# Install Datadog Agent
DD_API_KEY=your_api_key_here \
DD_SITE="datadoghq.com" \
bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh)"

# Set tags for correlation
cat <<EOF > /etc/datadog-agent/datadog.yaml
api_key: your_api_key_here
site: datadoghq.com
tags:
  - env:prod
  - service:checkout
  - team:core-reliability
EOF

systemctl restart datadog-agent
```

## ✅ 5. Verifying in Datadog
1.  Go to **Infrastructure List**.
2.  Search for `service:checkout`.
3.  Ensure you see `aws.ec2.cpu` metrics arriving via the Agent.
