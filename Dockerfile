FROM python:3.9-slim

# Metadata
LABEL base.image="python:3.9-slim"
LABEL version="1.0.3"
LABEL software="JLOH"
LABEL description="A tool to extract, filter, and manage blocks of loss of heterozygosity (LOH) based on single-nucleotide polymorphisms (SNPs), read mapping, and a reference genome"
LABEL website="https://github.com/MahShaaban/jloh"
LABEL license="GNU General Public License 3.0"
LABEL maintainer="Matteo Schiavinato (BSC): JLOH developer, Diego Fuentes (BSC): Docker image developer"

# Set up bash shell
SHELL ["/bin/bash", "-c"]

# Update system and install system dependencies
RUN apt-get update -qq && \
    apt-get install -y \
        build-essential \
        git \
        wget \
        curl \
        samtools \
        bedtools \
        mummer \
        r-base \
        default-jre \
        perl \
        && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN python -m pip install --upgrade pip

# Install core Python packages
RUN pip install --no-cache-dir \
    "numpy>=1.20.0" \
    "pandas>=1.3.0" \
    "matplotlib>=3.3.0" \
    "seaborn>=0.11.0" \
    "scipy>=1.7.0" \
    "biopython>=1.78"

# Install bioinformatics Python packages
RUN pip install --no-cache-dir \
    "pysam>=0.16.0" \
    "pybedtools>=0.8.0"

# Install additional Python packages for testing
RUN pip install --no-cache-dir \
    "pytest>=6.0" \
    "pytest-cov"

# Install R packages
RUN R -e "install.packages(c('ggplot2', 'reshape2', 'hash', 'scales', 'png'), repos='https://cran.r-project.org')"

# Install HISAT2
RUN apt-get update -qq && \
    apt-get install -y hisat2

# Install additional tools that might be needed
WORKDIR /tmp

# Clone and install JLOH from GitHub pkg branch
WORKDIR /opt
RUN git clone -b pkg https://github.com/MahShaaban/jloh.git && \
    cd jloh && \
    pip install -e .

# Create jloh executable wrapper
RUN echo '#!/bin/bash' > /usr/local/bin/jloh && \
    echo 'python /opt/jloh/jloh/cli.py "$@"' >> /usr/local/bin/jloh && \
    chmod +x /usr/local/bin/jloh

# Set working directory
WORKDIR /data

# Add jloh to PATH
ENV PATH="/usr/local/bin:${PATH}"

# Test installation
RUN jloh --help || true

# Set default command
CMD ["jloh", "--help"]
