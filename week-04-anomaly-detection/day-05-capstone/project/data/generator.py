import numpy as np
import pandas as pd
import random
import time

class MetricGenerator:
    def __init__(self):
        self.t = 0
        
    def generate_history(self, days=30):
        """Generates 30 days of normal traffic (1-min intervals)"""
        n_steps = days * 24 * 60
        dates = pd.date_range(start='2025-01-01', periods=n_steps, freq='T')
        
        # 1. Base Traffic (Sine Wave)
        hour_of_day = dates.hour
        # Peak at 14:00 (2 PM), Trough at 02:00 (2 AM)
        base = 50 + 30 * np.sin(2 * np.pi * (hour_of_day - 8) / 24)
        
        # 2. Trend (Slow Linear Growth)
        trend = np.linspace(0, 5, n_steps)
        
        # 3. Noise
        noise = np.random.normal(0, 2, n_steps)
        
        # Combine
        cpu = base + trend + noise
        
        # Clip to 0-100
        cpu = np.clip(cpu, 0, 100)
        
        # Add a Fan Speed metric (Inverse Correlated with CPU normally)
        # Actually, Fan usually goes UP when CPU goes UP.
        # Let's say correlated.
        fan = cpu * 20 + np.random.normal(0, 50, n_steps) # ~1000 RPM at 50% CPU
        fan = np.clip(fan, 0, 5000)
        
        df = pd.DataFrame({
            'timestamp': dates,
            'cpu': cpu,
            'fan_speed': fan
        })
        return df

    def stream_live(self, n_events=100):
        """Yields live events with injected attacks"""
        # Start where history ended (conceptually)
        current_time = pd.Timestamp('2025-01-31 00:00:00')
        
        # Define Attack Schedule (indices 20, 40, 60, 80, 95)
        # We simulate 100 minutes
        attack_map = {
            20: 'slow_burn',   # Cpu creeps up fast
            40: 'flash_crash', # Cpu drops to 0
            60: 'night_raid',  # High CPU at 3 AM (we force time)
            80: 'cooldown',    # CPU High, Fan Low (Broken Correlation)
            95: 'heart_attack' # Flatline variance
        }
        
        for i in range(n_events):
            # Normal baseline
            base_cpu = 50 # simplified
            base_fan = 1000
            
            # Helper to get contextual hour
            # We simulate time passing
            event_time = current_time + pd.Timedelta(minutes=i)
            hour = event_time.hour
            
            # Default Normal
            cpu = base_cpu + np.random.normal(0, 2)
            fan = cpu * 20 + np.random.normal(0, 50)
            label = 'normal'
            
            # Injection Logic
            attack_type = attack_map.get(i)
            
            if attack_type == 'slow_burn':
                # Trend outlier
                cpu = 95 
                fan = cpu * 20
                label = 'slow_burn'
                
            elif attack_type == 'flash_crash':
                # Point outlier
                cpu = 0
                fan = 0
                label = 'flash_crash'
                
            elif attack_type == 'night_raid':
                # Context intruder
                # Force time to be 3 AM
                # Normally 3 AM cpu is ~20. We send 80.
                event_time = event_time.replace(hour=3)
                cpu = 80
                fan = 1600
                label = 'night_raid'
                
            elif attack_type == 'cooldown':
                # Correlation break
                cpu = 90
                fan = 500 # Should be ~1800
                label = 'cooldown'
                
            elif attack_type == 'heart_attack':
                # Zero variance
                cpu = 50.0001
                fan = 1000.0001
                label = 'heart_attack'

            yield {
                'timestamp': event_time,
                'cpu': cpu,
                'fan_speed': fan,
                'label': label # Ground Truth for game scoring
            }
            time.sleep(0.01) # Simulate Latency

if __name__ == "__main__":
    gen = MetricGenerator()
    print("Generating History...")
    df = gen.generate_history()
    df.to_csv('history.csv', index=False)
    print("Saved history.csv")
