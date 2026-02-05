import numpy as np
import pandas as pd

def generate_cost_features(days=365):
    """
    Generates synthetic cloud cost data.
    Components:
    1. Baseline: Fixed infrastructure cost.
    2. Trend: Linear growth (more users).
    3. Seasonality: Weekly cycle (lower on weekends).
    4. Noise: Random fluctuation.
    """
    np.random.seed(42)
    dates = pd.date_range(start='2025-01-01', periods=days)
    
    # 1. Baseline ($1000/day)
    baseline = 1000
    
    # 2. Trend (+$5/day)
    trend = np.linspace(0, 5*days, days)
    
    # 3. Seasonality (Shape = Week)
    # Mon=0 ... Sun=6
    day_of_week = dates.dayofweek
    # Multiplier: 1.0 on weekdays, 0.8 on weekends
    seasonality_mult = np.where(day_of_week >= 5, 0.8, 1.0)
    
    # 4. Noise
    noise = np.random.normal(0, 50, days)
    
    # Combine
    # Base + Trend is the "Potential" usage
    # Seasonality scales that usage
    daily_cost = (baseline + trend) * seasonality_mult + noise
    
    df = pd.DataFrame({
        'Date': dates,
        'Daily_Cost': daily_cost.round(2)
    })
    
    return df

if __name__ == "__main__":
    print("Generating synthetic AWS cost data...")
    df = generate_cost_features(days=730) # 2 years
    
    filename = "aws_costs.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} rows to {filename}")
    print(df.head())
