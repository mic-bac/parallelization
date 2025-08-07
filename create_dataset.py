
"""
create_dataset.py
-----------------
Generate a large random dataset and save it as a CSV file.

Usage:
    python create_dataset.py
"""

import pandas as pd
import numpy as np

def generate_dataset(rows=1_000_000, cols=10, filename="big_data.csv"):
    """
    Generate a random dataset and save it as a CSV file.

    Args:
        rows (int): Number of rows in the dataset.
        cols (int): Number of columns in the dataset.
        filename (str): Output CSV filename.
    """
    print(f"Generating random dataset: {rows} rows x {cols} columns...")
    data = np.random.rand(rows, cols)
    df = pd.DataFrame(data, columns=[f"col{i}" for i in range(1, cols + 1)])
    print(f"Saving to '{filename}' (this may take a moment)...")
    df.to_csv(filename, index=False)
    print(f"Done! File saved: {filename} (~{round(df.memory_usage(deep=True).sum() / 1e6, 1)} MB in memory)")

if __name__ == "__main__":
    generate_dataset()
