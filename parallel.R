# -------------------------------------------------------------
# Parallelization in R: Serial vs. Parallel vs. Vectorized
# This script demonstrates how to process large datasets in R
# using serial, parallel, and vectorized approaches.
# -------------------------------------------------------------

# --- 1. Load required package ---
library(parallel)

# --- 2. Load the dataset ---
cat("Loading dataset... (this may take a moment)\n")
df <- read.csv("big_data.csv")
cat(sprintf("Dataset shape: %d rows x %d columns\n", nrow(df), ncol(df)))

# --- 3. Define a slow row operation ---
# This function simulates a heavy computation for each row.
expensive_row_op <- function(row) {
  Sys.sleep(0.00001)  # Simulate work (0.01ms per row)
  mean(as.numeric(row))
}

# --- 4. Convert DataFrame to matrix for faster row access ---
data <- as.matrix(df)

# --- 5. Serial computation (no parallelization) ---
cat("\n--- Serial computation (apply) ---\n")
time_start <- Sys.time()
results_serial <- apply(data, 1, expensive_row_op)
time_end <- Sys.time()
cat(sprintf("Serial time: %.2f seconds\n", as.numeric(difftime(time_end, time_start, units="secs"))))

# --- 6. Parallel computation using mclapply ---
cat("\n--- Parallel computation (mclapply) ---\n")
n_cpu <- detectCores()
cat(sprintf("Number of CPU cores available: %d\n", n_cpu))
n_cpu <- min(4, n_cpu)  # Use up to 4 cores (leave some for system)
cat(sprintf("Using %d cores for parallel computation.\n", n_cpu))

time_start <- Sys.time()
results_parallel <- unlist(mclapply(
  split(data, seq(nrow(data))),
  function(row) expensive_row_op(matrix(row, nrow=1)),
  mc.cores = n_cpu
))
time_end <- Sys.time()
cat(sprintf("Parallel time: %.2f seconds\n", as.numeric(difftime(time_end, time_start, units="secs"))))

# --- 7. Fastest: Vectorized computation ---
cat("\n--- Fastest: Vectorized rowMeans ---\n")
time_start <- Sys.time()
row_means <- rowMeans(data)
time_end <- Sys.time()
cat(sprintf("Time taken with optimized rowMeans: %.2f seconds\n", as.numeric(difftime(time_end, time_start, units="secs"))))

# --- 8. Summary ---
cat("\nSummary:\n")
cat("- Serial (apply): Slowest, processes one row at a time in R.\n")
cat("- Parallel (mclapply): Faster, splits work across CPU cores.\n")
cat("- Vectorized (rowMeans): Fastest, uses optimized C code under the hood.\n")
cat("\nFor real-world heavy computations, parallelization can greatly speed up your code!\n")