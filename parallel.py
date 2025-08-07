import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count

# Load the dataset
df = pd.read_csv('big_data.csv')

# Function to compute mean of a row
def row_mean(row):
    return np.mean(row)

if __name__ == '__main__':
    # Convert dataframe to numpy array for speed
    data = df.values

    # Start the pool
    with Pool(cpu_count()) as pool:
        results = pool.map(row_mean, data)

    # Convert result to pandas Series
    row_means = pd.Series(results)
    print(row_means.head())
