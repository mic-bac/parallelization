import pandas as pd
import numpy as np

# Generate 1M x 10 matrix
data = np.random.rand(1_000_000, 10)

# Save to CSV
df = pd.DataFrame(data, columns=[f"col{i}" for i in range(1, 11)])
df.to_csv("big_data.csv", index=False)
