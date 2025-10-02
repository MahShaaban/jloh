#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the README file for the long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "JLOH - A tool for Loss of Heterozygosity analysis"

# Read requirements
def read_requirements():
    try:
        with open("requirements-dev.txt", "r") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

setup(
    name="jloh",
    version="1.0.3",
    author="Matteo Schiavinato",
    author_email="matteo.schiavinato.90@gmail.com",
    description="A tool to extract, filter, and manage blocks of loss of heterozygosity (LOH)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/MahShaaban/jloh",
    packages=["jloh", "jloh.functions"],  # Explicitly specify packages
    py_modules=["cli"],  # Include the root cli.py module
    package_dir={"": "."},  # Packages are in the root directory
    include_package_data=True,
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "matplotlib>=3.3.0",
        "seaborn>=0.11.0",
        "scipy>=1.7.0",
        "biopython>=1.78",
        "pysam>=0.16.0",
        "pybedtools>=0.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
        ]
    },
    entry_points={
        "console_scripts": [
            "jloh=cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.9",
    zip_safe=False,
)