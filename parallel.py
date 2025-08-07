"""
parallel.py
-----------
Demonstration of serial vs. parallel computation in Python using a large dataset.
This script is structured as a notebook for students new to parallelization.
"""

# %% [markdown]
# # Parallelization in Python: Serial vs. Parallel vs. Vectorized
# This notebook demonstrates how to process large datasets using different approaches in Python.
# We'll compare serial (for loop), parallel (multiprocessing), and vectorized (numpy) methods.

# %%
# --- 1. Imports ---
from time import time, sleep
import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count

# %% [markdown]
# ## Load the Dataset
# We'll use a large CSV file with random numbers. Make sure `big_data.csv` exists in your folder.

# %%
# --- 2. Load the dataset ---
print("Loading dataset... (this may take a moment)")
df = pd.read_csv('big_data.csv')
print(f"Dataset shape: {df.shape}")

# %% [markdown]
# ## Define a Slow Row Operation
# We'll use a function that simulates a heavy computation for each row (e.g., a slow function).

# %%
# --- 3. Define a slow row operation ---
def expensive_row_op(row):
    """
    Simulate a heavy computation for each row (e.g., a slow function).
    """
    sleep(0.00001)  # Simulate work (0.01ms per row)
    return np.mean(row)

# %% [markdown]
# ## Convert DataFrame to Numpy Array
# This makes row-wise operations much faster.

# %%
# --- 4. Convert DataFrame to numpy array for faster row access ---
data = df.values

# %% [markdown]
# ## Serial Computation (for loop)
# This is the slowest method, as it processes one row at a time.

# %%
# --- 5. Serial computation (no parallelization) ---
print("\n--- Serial computation (for loop) ---")
time_start = time()
results_serial = [expensive_row_op(row) for row in data]
time_end = time()
print(f"Serial time: {time_end - time_start:.2f} seconds")

# %% [markdown]
# ## Parallel Computation (multiprocessing.Pool)
# This method splits the work across multiple CPU cores.

# %%
# --- 6. Parallel computation using multiprocessing ---
print("\n--- Parallel computation (multiprocessing.Pool) ---")
n_cpu = cpu_count()
print(f"Number of CPUs available: {n_cpu}")
n_cpu = min(6, n_cpu)  # Reserve some CPUs for other tasks
print(f"Using {n_cpu} processes for parallel computation.")

time_start = time()
with Pool(n_cpu) as pool:
    results_parallel = pool.map(expensive_row_op, data)
time_end = time()
print(f"Parallel time: {time_end - time_start:.2f} seconds")

# %% [markdown]
# ## Fastest: Vectorized Numpy Operation
# For built-in functions like mean, numpy can process all rows at once using optimized C code.

# %%
# --- 7. Fastest: Built-in vectorized numpy operation (no Python loop) ---
print("\n--- Fastest: Vectorized numpy operation ---")
time_start = time()
row_means = np.mean(data, axis=1)
time_end = time()
print(f"Numpy vectorized time: {time_end - time_start:.2f} seconds")

# %% [markdown]
# ## Summary
# - **Serial (for loop):** Slowest, processes one row at a time in Python.
# - **Parallel (multiprocessing):** Faster, splits work across CPU cores.
# - **Numpy vectorized:** Fastest, uses optimized C code under the hood.
#
# For real-world heavy computations, parallelization can greatly speed up your code!
