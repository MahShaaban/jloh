#!/usr/bin/env python3

"""
CLI interface for JLOH package maintaining backward compatibility.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def get_module_path(module_name):
    """Get the path to a JLOH module."""
    # Get the directory where this CLI script is located
    cli_dir = Path(__file__).parent
    
    # Look for the module in the same directory
    module_path = cli_dir / f"{module_name}.py"
    
    if module_path.exists():
        return str(module_path)
    
    # If not found, raise an error
    raise FileNotFoundError(f"Module '{module_name}' not found")


def show_help():
    """Display the JLOH help message."""
    help_text = """
    JLOH 
    Matteo Schiavinato
    Barcelona Supercomputing Center (BSC) 
    2023 
    contact: matteo.schiavinato.90@gmail.com

    v1.1.0

    ####

 -- Extraction
    stats               Estimate heterozygous and homozygous SNP statistics
    g2g                 Align two genomes to find regions that should carry SNPs
    extract             Extract LOH blocks from VCF, BAM and FASTA files
    onco_extract        Extract LOH blocks from VCF, BAM and FASTA files in a tumor context

 -- Operations
    filter              Filter extracted LOH blocks
    intersect           Perform intersection/removal operations with output files
    cluster             Cluster different runs by overlap 
    chimeric            Extract genes featuring LOH blocks from different haplotypes
    junctions           Calculate number of block-to-block junctions over the genome

 -- Visualization
    plot                Make an LOH propensity plot from "extract" output file(s)

 -- Simulation
    sim                 Simulate a divergent copy of a genome

"""
    print(help_text)


def main():
    """Main CLI entry point."""
    # If no arguments or help requested, show help
    if len(sys.argv) == 1:
        show_help()
        return
    
    if sys.argv[1] in ["--help", "-h", "-help", "help", "getopt", "usage"]:
        show_help()
        return
    
    # Get the module name and arguments
    module_name = sys.argv[1]
    module_args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    try:
        # Get the path to the module
        module_path = get_module_path(module_name)
        
        # Execute the module
        cmd = ["python3", module_path] + module_args
        result = subprocess.run(cmd, capture_output=False)
        
        # Exit with the same code as the module
        sys.exit(result.returncode)
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(f"Available modules: stats, g2g, extract, onco_extract, filter, intersect, cluster, chimeric, junctions, plot, sim", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running module '{module_name}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
