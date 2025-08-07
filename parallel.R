library(parallel)

# Load the dataset
df <- read.csv("big_data.csv")

# Function to compute mean of a row
row_mean <- function(row) {
  mean(as.numeric(row))
}

# Number of cores
num_cores <- detectCores()

# Apply in parallel
results <- mclapply(1:nrow(df), function(i) row_mean(df[i, ]), mc.cores = num_cores)

# Convert to vector
row_means <- unlist(results)
print(head(row_means))
