import numpy as np
import pandas as pd

def generate_bearing_data(n_steps=10000):
    """
    Simulates degrading bearing sensor data.
    4 Sensors: Vib_X, Vib_Y, Temp, Power.
    Phases: Healthy -> Degrading -> Critical.
    """
    np.random.seed(42)
    time = np.arange(n_steps)
    
    # 1. Healthy Phase (0-6000)
    # Steady noise
    vib_x = np.random.normal(0, 1, n_steps)
    vib_y = np.random.normal(0, 1, n_steps)
    temp = 50 + 5 * np.sin(time / 500) # Daily cycle
    power = temp * 2 + np.random.normal(0, 5, n_steps)
    
    # 2. Degrading Phase (6000-8000)
    # Variance increases linear
    degrade_mask = (time >= 6000) & (time < 8000)
    degrade_factor = (time[degrade_mask] - 6000) / 2000 # 0 -> 1
    
    vib_x[degrade_mask] *= (1 + 5 * degrade_factor) # Std 1 -> 6
    vib_y[degrade_mask] *= (1 + 5 * degrade_factor)
    temp[degrade_mask] += 20 * degrade_factor # Temp rises
    
    # 3. Critical Phase (8000+)
    # Chaos
    crit_mask = time >= 8000
    vib_x[crit_mask] *= 10
    vib_y[crit_mask] *= 10
    temp[crit_mask] += 50
    power[crit_mask] *= 1.5
    
    df = pd.DataFrame({
        'timestamp': time,
        'vib_x': vib_x,
        'vib_y': vib_y,
        'temp': temp,
        'power': power
    })
    
    return df

print("Generating Bearing Sensor Data...")
df = generate_bearing_data()
df.to_csv('sensor_logs.csv', index=False)
print("Saved to sensor_logs.csv")
