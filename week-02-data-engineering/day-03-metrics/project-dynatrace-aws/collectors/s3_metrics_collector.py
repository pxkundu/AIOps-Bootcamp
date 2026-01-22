#!/usr/bin/env python3
"""
AWS S3 Metrics Collector for Dynatrace
Collects standard S3 metrics from CloudWatch and forwards to Dynatrace
"""

import boto3
import requests
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Initialize AWS clients
s3 = boto3.client('s3')
cloudwatch = boto3.client('cloudwatch')

# Dynatrace configuration
DYNATRACE_URL = os.environ.get('DYNATRACE_URL', 'https://your-environment.live.dynatrace.com')
DYNATRACE_API_TOKEN = os.environ.get('DYNATRACE_API_TOKEN')

def lambda_handler(event, context):
    """Lambda handler for scheduled execution"""
    try:
        metrics_count = collect_and_send_s3_metrics()
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully collected {metrics_count} S3 metrics',
                'timestamp': datetime.utcnow().isoformat()
            })
        }
    except Exception as e:
        print(f"Error collecting S3 metrics: {str(e)}")
        raise

def collect_and_send_s3_metrics() -> int:
    """Main function to collect S3 metrics and send to Dynatrace"""
    
    # Get all S3 buckets
    buckets = get_all_s3_buckets()
    
    # Collect metrics for each bucket
    all_metrics = []
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    
    for bucket in buckets:
        bucket_name = bucket['Name']
        bucket_region = bucket.get('Region', 'us-east-1')
        
        bucket_metrics = collect_bucket_metrics(bucket_name, bucket_region, start_time, end_time)
        all_metrics.extend(bucket_metrics)
    
    # Send to Dynatrace
    if all_metrics:
        send_to_dynatrace(all_metrics)
    
    return len(all_metrics)

def get_all_s3_buckets() -> List[Dict[str, Any]]:
    """Get all S3 buckets in the account"""
    buckets = []
    try:
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            # Get bucket location
            try:
                location = s3.get_bucket_location(Bucket=bucket['Name'])
                region = location.get('LocationConstraint') or 'us-east-1'
            except:
                region = 'us-east-1'
            
            buckets.append({
                'Name': bucket['Name'],
                'Region': region,
                'CreationDate': bucket['CreationDate']
            })
    except Exception as e:
        print(f"Error listing buckets: {e}")
    
    return buckets

def collect_bucket_metrics(bucket_name: str, region: str, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
    """Collect metrics for a specific S3 bucket"""
    metrics = []
    
    # Standard S3 metrics to collect
    metric_definitions = [
        {
            'metric_name': 'BucketSizeBytes',
            'dynatrace_id': 'aws.s3.bucket_size',
            'dimensions': [
                {'Name': 'BucketName', 'Value': bucket_name},
                {'Name': 'StorageType', 'Value': 'StandardStorage'}
            ],
            'statistics': ['Average'],
            'period': 3600  # Hourly for bucket size
        },
        {
            'metric_name': 'NumberOfObjects',
            'dynatrace_id': 'aws.s3.number_of_objects',
            'dimensions': [
                {'Name': 'BucketName', 'Value': bucket_name},
                {'Name': 'StorageType', 'Value': 'AllStorageTypes'}
            ],
            'statistics': ['Average'],
            'period': 3600
        },
        {
            'metric_name': 'AllRequests',
            'dynatrace_id': 'aws.s3.all_requests',
            'dimensions': [{'Name': 'BucketName', 'Value': bucket_name}],
            'statistics': ['Sum'],
            'period': 300
        },
        {
            'metric_name': 'GetRequests',
            'dynatrace_id': 'aws.s3.get_requests',
            'dimensions': [{'Name': 'BucketName', 'Value': bucket_name}],
            'statistics': ['Sum'],
            'period': 300
        },
        {
            'metric_name': 'PutRequests',
            'dynatrace_id': 'aws.s3.put_requests',
            'dimensions': [{'Name': 'BucketName', 'Value': bucket_name}],
            'statistics': ['Sum'],
            'period': 300
        },
        {
            'metric_name': 'DeleteRequests',
            'dynatrace_id': 'aws.s3.delete_requests',
            'dimensions': [{'Name': 'BucketName', 'Value': bucket_name}],
            'statistics': ['Sum'],
            'period': 300
        },
        {
            'metric_name': 'BytesDownloaded',
            'dynatrace_id': 'aws.s3.bytes_downloaded',
            'dimensions': [{'Name': 'BucketName', 'Value': bucket_name}],
            'statistics': ['Sum'],
            'period': 300
        },
        {
            'metric_name': 'BytesUploaded',
            'dynatrace_id': 'aws.s3.bytes_uploaded',
            'dimensions': [{'Name': 'BucketName', 'Value': bucket_name}],
            'statistics': ['Sum'],
            'period': 300
        },
        {
            'metric_name': '4xxErrors',
            'dynatrace_id': 'aws.s3.4xx_errors',
            'dimensions': [{'Name': 'BucketName', 'Value': bucket_name}],
            'statistics': ['Sum'],
            'period': 300
        },
        {
            'metric_name': '5xxErrors',
            'dynatrace_id': 'aws.s3.5xx_errors',
            'dimensions': [{'Name': 'BucketName', 'Value': bucket_name}],
            'statistics': ['Sum'],
            'period': 300
        }
    ]
    
    for metric_def in metric_definitions:
        try:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName=metric_def['metric_name'],
                Dimensions=metric_def['dimensions'],
                StartTime=start_time,
                EndTime=end_time,
                Period=metric_def['period'],
                Statistics=metric_def['statistics']
            )
            
            # Convert CloudWatch datapoints to Dynatrace format
            for datapoint in response.get('Datapoints', []):
                value = datapoint.get('Sum') or datapoint.get('Average', 0)
                
                metrics.append({
                    'metricId': metric_def['dynatrace_id'],
                    'value': value,
                    'timestamp': int(datapoint['Timestamp'].timestamp() * 1000),
                    'dimensions': {
                        'bucket_name': bucket_name,
                        'aws_region': region
                    }
                })
        except Exception as e:
            print(f"Error collecting {metric_def['metric_name']} for {bucket_name}: {e}")
            continue
    
    return metrics

def send_to_dynatrace(metrics: List[Dict[str, Any]]) -> None:
    """Send metrics to Dynatrace Metrics API v2"""
    if not DYNATRACE_API_TOKEN:
        raise ValueError("DYNATRACE_API_TOKEN environment variable not set")
    
    url = f"{DYNATRACE_URL}/api/v2/metrics/ingest"
    
    headers = {
        'Authorization': f'Api-Token {DYNATRACE_API_TOKEN}',
        'Content-Type': 'text/plain; charset=utf-8'
    }
    
    # Format metrics as Dynatrace ingest format
    lines = []
    for metric in metrics:
        dims = ','.join([f"{k}={v}" for k, v in metric['dimensions'].items()])
        line = f"{metric['metricId']},{dims} {metric['value']} {metric['timestamp']}"
        lines.append(line)
    
    payload = '\n'.join(lines)
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        response.raise_for_status()
        print(f"Successfully sent {len(metrics)} metrics to Dynatrace")
    except requests.exceptions.RequestException as e:
        print(f"Error sending metrics to Dynatrace: {e}")
        print(f"Response: {response.text if 'response' in locals() else 'N/A'}")
        raise

if __name__ == '__main__':
    # For local testing
    count = collect_and_send_s3_metrics()
    print(f"Collected and sent {count} S3 metrics to Dynatrace")
