
# Parallelization

Examples for parallelization using Python and R.

## Setup

This project demonstrates parallelization using Python and R, managed with Conda and Quarto on Ubuntu WSL.

### 1. Install Conda in WSL

```bash
# Download Miniconda installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Run installer
bash Miniconda3-latest-Linux-x86_64.sh

# Follow the prompts, then activate Conda
source ~/.bashrc

# If 'conda' is not found, add it to your .bashrc
<PATH-TO-CONDA>/bin/conda init bash

# Confirm installation
conda --version
```

### 2. Create the Conda Environment

```bash
conda env create -f conda-env.yml

# activate the environment after creation
conda activate parallel
```
Make sure to replace `parallel` with the name of your environment if it differs.

Check if the environment is activated:

```bash
# Check active environments (active environment will be marked with an asterisk)
conda info --envs
```

### 3. Install R packages for VSCode

```bash
# For more handy packages see VSCode documentation for using R in VSCode
R --quiet -e "install.packages(c('languageserver'), repos='https://cloud.r-project.org')"
```
