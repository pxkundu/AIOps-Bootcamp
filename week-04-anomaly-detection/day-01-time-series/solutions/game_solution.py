# Solution for "The Time Fixer" Verification Game
# Week 4 Day 1 Gamification

import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

def fix_the_jitter(df):
    """Level 1: Fix irregular timestamps"""
    print("Level 1: Fixing Jitter -> Resampling...")
    # Resample to regular 1-min intervals
    return df.resample('1min').mean()

def fix_the_void(df):
    """Level 2: Fix missing data"""
    print("Level 2: Fixing Void -> Interpolating...")
    # Fill gaps linearly based on time
    return df.interpolate(method='time')

def fix_the_drift(df):
    """Level 3: Fix non-stationary trend"""
    print("Level 3: Fixing Drift -> Differencing...")
    # Remove trend by subtracting previous value
    return df.diff().dropna()

def fix_the_ghost(df):
    """Level 4: Fix seasonality"""
    print("Level 4: Fixing Ghost -> Deseasonalizing...")
    # Decompose and return only Trend + Residual (subtract Seasonality)
    decomp = seasonal_decompose(df, model='additive', period=1440)
    return df - decomp.seasonal

def fix_the_fog(df):
    """Level 5: Fix noise"""
    print("Level 5: Fixing Fog -> Rolling Mean...")
    # Smooth out high-frequency noise
    return df.rolling(window=10).mean()

# Mock Game Runner
if __name__ == "__main__":
    # Create dummy data
    dates = pd.date_range('2026-01-01', periods=2000, freq='T')
    data = np.random.randn(2000).cumsum() # Random walk (Drift)
    df = pd.Series(data, index=dates)
    
    # Run the levels
    df_clean = fix_the_jitter(df)
    df_clean = fix_the_void(df_clean)
    
    # Check Drift
    from statsmodels.tsa.stattools import adfuller
    print(f"Original p-value: {adfuller(df_clean.dropna())[1]:.4f}")
    
    df_stationary = fix_the_drift(df_clean)
    print(f"Fixed p-value: {adfuller(df_stationary)[1]:.4f}")
    
    print("\n🏆 MISSION ACCOMPLISHED: TIMELINE STABILIZED 🏆")
