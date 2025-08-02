# Parallelization
Examples for parallelization using python and R

## Setup
To illustrate how parallelization works using python and R we'll use a conda environment manager and quarto running on Ubuntu wSL.

Here is the setup definition:

Install Conda in WSL

```bash
# Download installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Run installer
bash Miniconda3-latest-Linux-x86_64.sh

# Follow the prompts, then:
source ~/.bashrc

# TROUBLESHOOT if conda command is not found
# Replace <PATH-TO-CONDA> with the file path to your conda installation to add it to .bashrc file
<PATH-TO-CONDA>/bin/conda init bash

# Confirm it is working
conda --version
```

## Create the environment

```bash
# create the conda environment
conda env create -f conda-env.yml

# Install IRkernel from R
R --quiet -e "install.packages('IRkernel'); IRkernel::installspec(user = FALSE)"

# Check and list all installed kernels
jupyter kernelspec list
```

## Install quarto
```bash
# Install
wget https://quarto.org/download/latest/quarto-linux-amd64.deb
sudo dpkg -i quarto-linux-amd64.deb

# Check installation
quarto check
```

## Set-up variable sharing
Install rpy2 in the conda environment