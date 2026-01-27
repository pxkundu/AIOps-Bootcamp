import pandas as pd
import numpy as np
import boto3
import io
import os
from sklearn.preprocessing import StandardScaler

# Initialize S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda handler for the AIOps Data Refinery.
    Triggers on S3 bucket uploads and performs EDA/Preprocessing.
    """
    try:
        # 1. Extract bucket and key from the event
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        dest_bucket = os.environ.get('DEST_BUCKET')
        
        if not dest_bucket:
            raise ValueError("Environment variable DEST_BUCKET is not set.")

        print(f"Processing file: {key} from bucket: {source_bucket}")

        # 2. Read the raw data from S3
        response = s3_client.get_object(Bucket=source_bucket, Key=key)
        data_content = response['Body'].read()
        df = pd.read_csv(io.BytesIO(data_content))

        # --- AIOps PREPROCESSING (Week 3 Day 2) ---
        
        # 3. Handle Missing Values
        # Using linear interpolation for time-series continuity
        df.interpolate(method='linear', inplace=True)
        # Forward fill for any remaining NaNs at the start/end
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)

        # 4. Feature Scaling (Standardization)
        # Ensures features like CPU (0-100) and Latency (0-5000) are comparable
        scaler = StandardScaler()
        # Identify numeric columns, excluding timestamp if it's there
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        # 5. Cyclic Feature Engineering
        # Capture periodicity of daily/weekly ops cycles
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            # Normalize hour to 0-2pi and take sin/cos
            df['hour_sin'] = np.sin(2 * np.pi * df['timestamp'].dt.hour / 24)
            df['hour_cos'] = np.cos(2 * np.pi * df['timestamp'].dt.hour / 24)
            # Add day of week flag
            df['is_weekend'] = df['timestamp'].dt.dayofweek.isin([5, 6]).astype(int)

        # 6. Convert refined DataFrame back to CSV
        output_buffer = io.StringIO()
        df.to_csv(output_buffer, index=False)

        # 7. Upload the refined data to the destination bucket
        output_key = f"refined/{key.split('/')[-1]}"
        s3_client.put_object(
            Bucket=dest_bucket,
            Key=output_key,
            Body=output_buffer.getvalue(),
            ContentType='text/csv'
        )

        print(f"Successfully refined data and uploaded to: {dest_bucket}/{output_key}")
        
        return {
            "statusCode": 200,
            "body": f"Successfully processed {key}"
        }

    except Exception as e:
        print(f"Error processing {key}: {str(e)}")
        return {
            "statusCode": 500,
            "body": str(e)
        }
