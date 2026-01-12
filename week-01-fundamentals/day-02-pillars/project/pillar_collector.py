import pandas as pd
import json
import os
import sys
from datetime import datetime

class PillarCollector:
    def __init__(self, cardinality_threshold=0.5):
        self.threshold = cardinality_threshold

    def analyze_metrics(self, file_path):
        """Analyzes a CSV metrics file for cardinality and basic validity."""
        print(f"\n📊 Analyzing Metrics: {file_path}")
        try:
            df = pd.read_csv(file_path)
            self._check_cardinality(df)
            print(f"✅ Samples checked: {len(df)}")
            return df
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def analyze_logs(self, file_path):
        """Analyzes a JSON lines logs file."""
        print(f"\n📝 Analyzing Logs: {file_path}")
        logs = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    logs.append(json.loads(line))
            df = pd.DataFrame(logs)
            self._check_cardinality(df)
            print(f"✅ Logs parsed: {len(df)}")
            return df
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def _check_cardinality(self, df):
        """Detects high cardinality columns."""
        total_rows = len(df)
        for col in df.columns:
            unique_values = df[col].nunique()
            ratio = unique_values / total_rows
            
            if ratio > self.threshold and total_rows > 10:
                print(f"⚠️  HIGH CARDINALITY WARNING: Column '{col}' has {unique_values} unique values ({ratio:.2%} unique)")
            else:
                print(f"🔹 Column '{col}': {unique_values} unique values")

    def correlate(self, metrics_df, logs_df):
        """Simple correlation based on timestamp overlap."""
        print("\n🔗 Attempting Correlation (Timestamp Overlap)...")
        if metrics_df is None or logs_df is None:
            return

        # Ensure timestamps are comparable
        metrics_df['ts_clean'] = pd.to_datetime(metrics_df['timestamp'])
        logs_df['ts_clean'] = pd.to_datetime(logs_df['timestamp']).dt.tz_localize(None)

        # Find overlaps (within 1 second)
        # Note: This is a simplified demo correlation
        merged = pd.merge_asof(
            metrics_df.sort_values('ts_clean'),
            logs_df.sort_values('ts_clean'),
            on='ts_clean',
            tolerance=pd.Timedelta('1s'),
            direction='nearest'
        ).dropna(subset=['level']) # Only keep rows that actually matched a log

        if not merged.empty:
            print(f"🎯 Found {len(merged)} correlated event pairs!")
            print(merged[['ts_clean', 'cpu_usage_pct', 'level', 'message']].head())
        else:
            print("📭 No immediate correlation found.")

def main():
    collector = PillarCollector()
    
    # Paths (Assumes running from project root)
    metrics_file = "../day-01-intro/resources/seasonal_metrics.csv"
    logs_file = "sample_logs.jsonl"
    
    # 1. Generate dummy logs if they don't exist
    if not os.path.exists(logs_file):
        print("Generating dummy logs...")
        from log_generator import generate_log
        with open(logs_file, 'w') as f:
            for _ in range(50):
                f.write(json.dumps(generate_log()) + "\n")

    # 2. Analyze
    m_df = collector.analyze_metrics(metrics_file)
    l_df = collector.analyze_logs(logs_file)
    
    # 3. Correlate
    collector.correlate(m_df, l_df)

if __name__ == "__main__":
    # Add parent dir to path so we can import generators if needed
    sys.path.append(os.path.abspath("../day-01-intro/resources"))
    main()
