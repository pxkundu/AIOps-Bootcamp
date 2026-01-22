#!/usr/bin/env python3
"""
AWS EC2 Metrics Collector for Dynatrace
Collects standard EC2 metrics from CloudWatch and forwards to Dynatrace
"""

import boto3
import requests
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Initialize AWS clients
ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

# Dynatrace configuration
DYNATRACE_URL = os.environ.get('DYNATRACE_URL', 'https://your-environment.live.dynatrace.com')
DYNATRACE_API_TOKEN = os.environ.get('DYNATRACE_API_TOKEN')

def lambda_handler(event, context):
    """Lambda handler for scheduled execution"""
    try:
        metrics_count = collect_and_send_ec2_metrics()
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully collected {metrics_count} EC2 metrics',
                'timestamp': datetime.utcnow().isoformat()
            })
        }
    except Exception as e:
        print(f"Error collecting EC2 metrics: {str(e)}")
        raise

def collect_and_send_ec2_metrics() -> int:
    """Main function to collect EC2 metrics and send to Dynatrace"""
    
    # Get all running EC2 instances
    instances = get_all_ec2_instances()
    
    # Collect metrics for each instance
    all_metrics = []
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)
    
    for instance in instances:
        instance_id = instance['InstanceId']
        instance_name = get_instance_name(instance)
        instance_type = instance.get('InstanceType', 'unknown')
        instance_region = os.environ.get('AWS_REGION', 'us-east-1')
        
        instance_metrics = collect_instance_metrics(
            instance_id, instance_name, instance_type, instance_region, start_time, end_time
        )
        all_metrics.extend(instance_metrics)
    
    # Send to Dynatrace
    if all_metrics:
        send_to_dynatrace(all_metrics)
    
    return len(all_metrics)

def get_all_ec2_instances() -> List[Dict[str, Any]]:
    """Get all running EC2 instances"""
    instances = []
    try:
        response = ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        
        for reservation in response['Reservations']:
            instances.extend(reservation['Instances'])
    except Exception as e:
        print(f"Error listing EC2 instances: {e}")
    
    return instances

def get_instance_name(instance: Dict[str, Any]) -> str:
    """Extract instance name from tags"""
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            return tag['Value']
    return instance['InstanceId']

def collect_instance_metrics(
    instance_id: str,
    instance_name: str,
    instance_type: str,
    region: str,
    start_time: datetime,
    end_time: datetime
) -> List[Dict[str, Any]]:
    """Collect metrics for a specific EC2 instance"""
    metrics = []
    dimensions = [{'Name': 'InstanceId', 'Value': instance_id}]
    
    # Standard EC2 metrics to collect
    metric_definitions = [
        {
            'metric_name': 'CPUUtilization',
            'dynatrace_id': 'aws.ec2.cpu_utilization',
            'statistics': ['Average'],
            'unit': 'Percent'
        },
        {
            'metric_name': 'NetworkIn',
            'dynatrace_id': 'aws.ec2.network_in',
            'statistics': ['Sum'],
            'unit': 'Bytes'
        },
        {
            'metric_name': 'NetworkOut',
            'dynatrace_id': 'aws.ec2.network_out',
            'statistics': ['Sum'],
            'unit': 'Bytes'
        },
        {
            'metric_name': 'DiskReadOps',
            'dynatrace_id': 'aws.ec2.disk_read_ops',
            'statistics': ['Sum'],
            'unit': 'Count'
        },
        {
            'metric_name': 'DiskWriteOps',
            'dynatrace_id': 'aws.ec2.disk_write_ops',
            'statistics': ['Sum'],
            'unit': 'Count'
        },
        {
            'metric_name': 'DiskReadBytes',
            'dynatrace_id': 'aws.ec2.disk_read_bytes',
            'statistics': ['Sum'],
            'unit': 'Bytes'
        },
        {
            'metric_name': 'DiskWriteBytes',
            'dynatrace_id': 'aws.ec2.disk_write_bytes',
            'statistics': ['Sum'],
            'unit': 'Bytes'
        },
        {
            'metric_name': 'StatusCheckFailed',
            'dynatrace_id': 'aws.ec2.status_check_failed',
            'statistics': ['Sum'],
            'unit': 'Count'
        },
        {
            'metric_name': 'StatusCheckFailed_Instance',
            'dynatrace_id': 'aws.ec2.status_check_failed_instance',
            'statistics': ['Sum'],
            'unit': 'Count'
        },
        {
            'metric_name': 'StatusCheckFailed_System',
            'dynatrace_id': 'aws.ec2.status_check_failed_system',
            'statistics': ['Sum'],
            'unit': 'Count'
        }
    ]
    
    for metric_def in metric_definitions:
        try:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName=metric_def['metric_name'],
                Dimensions=dimensions,
                StartTime=start_time,
                EndTime=end_time,
                Period=300,  # 5-minute intervals
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
                        'instance_id': instance_id,
                        'instance_name': instance_name,
                        'instance_type': instance_type,
                        'aws_region': region
                    }
                })
        except Exception as e:
            print(f"Error collecting {metric_def['metric_name']} for {instance_id}: {e}")
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
    count = collect_and_send_ec2_metrics()
    print(f"Collected and sent {count} EC2 metrics to Dynatrace")
