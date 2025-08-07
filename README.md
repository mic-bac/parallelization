
# 🚀 Parallelization Examples (Python & R)

> **A collection of examples demonstrating parallelization in Python and R, managed with Conda and Quarto on Ubuntu WSL.**

---

## 📦 Setup Instructions

### 1️⃣ Install Conda in WSL

```bash
# Download Miniconda installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Run the installer
bash Miniconda3-latest-Linux-x86_64.sh

# Reload your shell to activate Conda
source ~/.bashrc

# If 'conda' is not found, initialize it:
<PATH-TO-CONDA>/bin/conda init bash

# Confirm installation
conda --version
```

---

### 2️⃣ Create & Activate the Conda Environment

```bash
conda env create -f conda-env.yml

# Activate the environment after creation
conda activate parallel
```

> **Note:** Replace `parallel` with your environment name if it differs.

To check if the environment is activated:

```bash
# List all Conda environments (the active one is marked with an asterisk)
conda info --envs
```

---

## 📁 Project Structure

- `parallel.py` & `parallel.R` — Example scripts for parallelization in Python and R
- `create_dataset.py` — Script to generate a sample dataset
- `big_data.csv` — Example dataset
- `conda-env.yml` — Conda environment definition
- `README.md` — This file

---

## 📝 License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

