import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def encode_time(hours):
    # Map 0-23 into radians (0 to 2*pi)
    sin_feat = np.sin(2 * np.pi * hours / 24)
    cos_feat = np.cos(2 * np.pi * hours / 24)
    return sin_feat, cos_feat

hours = np.linspace(0, 23, 24)
s_sin, s_cos = encode_time(hours)

plt.figure(figsize=(6, 6))
plt.scatter(s_sin, s_cos, c=hours, cmap='hsv')
for i, h in enumerate(hours):
    plt.annotate(f"{int(h)}h", (s_sin[i], s_cos[i]))

plt.title("Cyclic Encoding of Time (Circle of Ops)")
plt.xlabel("Sine Feature")
plt.ylabel("Cosine Feature")
plt.grid(True)
plt.show()

print("Benefit: The difference between 23:00 and 00:00 is now represented accurately geographically.")
