#!/usr/bin/env python3
"""
AWS Lambda Metrics Collector for Dynatrace
Collects standard Lambda metrics from CloudWatch and forwards to Dynatrace
"""

import boto3
import requests
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Initialize AWS clients
cloudwatch = boto3.client('cloudwatch')
lambda_client = boto3.client('lambda')

# Dynatrace configuration
DYNATRACE_URL = os.environ.get('DYNATRACE_URL', 'https://your-environment.live.dynatrace.com')
DYNATRACE_API_TOKEN = os.environ.get('DYNATRACE_API_TOKEN')

def lambda_handler(event, context):
    """Lambda handler for scheduled execution"""
    try:
        metrics_count = collect_and_send_lambda_metrics()
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully collected {metrics_count} Lambda metrics',
                'timestamp': datetime.utcnow().isoformat()
            })
        }
    except Exception as e:
        print(f"Error collecting Lambda metrics: {str(e)}")
        raise

def collect_and_send_lambda_metrics() -> int:
    """Main function to collect Lambda metrics and send to Dynatrace"""
    
    # Get all Lambda functions
    functions = get_all_lambda_functions()
    
    # Collect metrics for each function
    all_metrics = []
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    
    for func in functions:
        function_name = func['FunctionName']
        function_metrics = collect_function_metrics(function_name, start_time, end_time)
        all_metrics.extend(function_metrics)
    
    # Send to Dynatrace
    if all_metrics:
        send_to_dynatrace(all_metrics)
    
    return len(all_metrics)

def get_all_lambda_functions() -> List[Dict[str, Any]]:
    """Get all Lambda functions in the account"""
    functions = []
    paginator = lambda_client.get_paginator('list_functions')
    
    for page in paginator.paginate():
        functions.extend(page['Functions'])
    
    return functions

def collect_function_metrics(function_name: str, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
    """Collect metrics for a specific Lambda function"""
    metrics = []
    dimensions = [{'Name': 'FunctionName', 'Value': function_name}]
    
    # Standard Lambda metrics to collect
    metric_definitions = [
        {
            'namespace': 'AWS/Lambda',
            'metric_name': 'Invocations',
            'dynatrace_id': 'aws.lambda.invocations',
            'statistics': ['Sum'],
            'unit': 'Count'
        },
        {
            'namespace': 'AWS/Lambda',
            'metric_name': 'Errors',
            'dynatrace_id': 'aws.lambda.errors',
            'statistics': ['Sum'],
            'unit': 'Count'
        },
        {
            'namespace': 'AWS/Lambda',
            'metric_name': 'Duration',
            'dynatrace_id': 'aws.lambda.duration',
            'statistics': ['Average'],
            'unit': 'Milliseconds'
        },
        {
            'namespace': 'AWS/Lambda',
            'metric_name': 'Throttles',
            'dynatrace_id': 'aws.lambda.throttles',
            'statistics': ['Sum'],
            'unit': 'Count'
        },
        {
            'namespace': 'AWS/Lambda',
            'metric_name': 'ConcurrentExecutions',
            'dynatrace_id': 'aws.lambda.concurrent_executions',
            'statistics': ['Maximum'],
            'unit': 'Count'
        },
        {
            'namespace': 'AWS/Lambda',
            'metric_name': 'DeadLetterErrors',
            'dynatrace_id': 'aws.lambda.dead_letter_errors',
            'statistics': ['Sum'],
            'unit': 'Count'
        }
    ]
    
    for metric_def in metric_definitions:
        try:
            response = cloudwatch.get_metric_statistics(
                Namespace=metric_def['namespace'],
                MetricName=metric_def['metric_name'],
                Dimensions=dimensions,
                StartTime=start_time,
                EndTime=end_time,
                Period=300,  # 5-minute intervals
                Statistics=metric_def['statistics']
            )
            
            # Convert CloudWatch datapoints to Dynatrace format
            for datapoint in response.get('Datapoints', []):
                # Use Sum for counters, Average for gauges
                value = datapoint.get('Sum') or datapoint.get('Average') or datapoint.get('Maximum', 0)
                
                metrics.append({
                    'metricId': metric_def['dynatrace_id'],
                    'value': value,
                    'timestamp': int(datapoint['Timestamp'].timestamp() * 1000),
                    'dimensions': {
                        'function_name': function_name,
                        'aws_region': os.environ.get('AWS_REGION', 'us-east-1')
                    }
                })
        except Exception as e:
            print(f"Error collecting {metric_def['metric_name']} for {function_name}: {e}")
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
    # Format: metricId,dimension1=value1,dimension2=value2 value timestamp
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
    count = collect_and_send_lambda_metrics()
    print(f"Collected and sent {count} Lambda metrics to Dynatrace")
