# JLOH Pipeline Case Study: Complete Workflow with Test Data

This case study demonstrates a complete JLOH analysis pipeline using the provided test data. We'll walk through the entire workflow from SNP statistics to visualization and downstream analysis.

## Overview

We'll analyze Loss of Heterozygosity (LOH) in *Saccharomyces paradoxuecho "  🔗 junction_stats.txt      : Junction analysis"
echo "  📈 plots/                  : LOH visualization plots"
echo "  🧪 S_para_chrXII_divergent.fa : Simulated genome"
echo "  📊 clustered_blocks.*.tsv  : Clustering results"
echo "  🔗 intersect_results.txt   : Intersection analysis"
echo "  🧬 g2g_results/            : Genome comparison"
echo ""
echo "⚠️  Note: Some features skipped due to current CLI limitations:"
echo "   - Chimeric gene analysis (requires two haplotype files)"
echo "   - Oncology analysis (parameter bug)"some XII using:
- **Reference genome**: `S_para.chrXII.fa` (chromosome XII, 1.02 Mb)
- **Variant calls**: `out.ff.vcf` (172 variants)
- **Read alignments**: `out.fs.bam` (with index)

## Prerequisites

```bash
# Activate the JLOH conda environment (ONCE - all subsequent commands run in this environment)
conda activate jloh

# Navigate to the JLOH directory
cd /path/to/jloh

# Install JLOH package in development mode (if not already installed)
pip install -e .

# Verify test data is present
ls test_data/
# Should show: S_para.chrXII.fa  out.ff.vcf  out.fs.bam  out.fs.bam.bai

# Verify JLOH CLI is working
jloh --help
```

## Step-by-Step Pipeline

### Step 1: SNP Statistics Analysis

First, let's analyze the SNP statistics to understand the variant landscape:

```bash
# Create output directory
mkdir -p case_study_output

# Run SNP statistics (outputs to stdout)
jloh stats \
    --vcf test_data/out.ff.vcf \
    --threads 2 \
    > case_study_output/snp_stats.txt
```

**Expected output**: Statistics on SNP density, coverage distribution, and variant quality metrics. The stats command only requires a VCF file and outputs results to stdout.

### Step 2: Extract LOH Blocks

Extract LOH blocks from the variant and alignment data:

```bash
# Extract LOH blocks using relaxed parameters for demo data
jloh extract \
    --vcf test_data/out.ff.vcf \
    --bam test_data/out.fs.bam \
    --ref test_data/S_para.chrXII.fa \
    --sample "S_para_chrXII" \
    --output-dir case_study_output/extract_results \
    --min-length 100 \
    --min-snps-kbp 1,0.5 \
    --threads 2

# Copy the results to a standard filename for subsequent steps
cp case_study_output/extract_results/S_para_chrXII.LOH_blocks.tsv case_study_output/loh_blocks.txt
```

**Parameters explained**:
- `--min-length 100`: Minimum LOH block length of 100 bp (relaxed for demo data)
- `--min-snps-kbp 1,0.5`: Minimum 1 SNPs/kbp for heterozygous, 0.5 SNP/kbp for homozygous regions (relaxed)
- `--sample`: Sample identifier for output files

**Note**: The parameters are relaxed compared to typical analysis to work with the limited test data.

### Step 3: Filter LOH Blocks

Filter the extracted blocks based on quality criteria:

```bash
# Filter blocks by length and SNP content
jloh filter \
    --loh case_study_output/loh_blocks.txt \
    --length 500 \
    --snps 3 \
    --coverage 5 \
    > case_study_output/loh_blocks_filtered.txt
```

**Filtering criteria**:
- Minimum block length: 500 bp
- Minimum SNPs per block: 3
- Minimum coverage: 5x

### Step 4: Analyze Block Junctions

Calculate junction statistics between LOH blocks:

```bash
# Analyze junctions between different allelic blocks
jloh junctions \
    --blocks case_study_output/loh_blocks_filtered.txt \
    --max-dist 5000 \
    --genome test_data/S_para.chrXII.fa \
    > case_study_output/junction_stats.txt
```

### Step 5: Create Visualization

Generate a visual representation of the LOH landscape:

```bash
# Create LOH plot using one-ref mode
# First, we need the heterozygous blocks file from the extract step
jloh plot \
    --one-ref \
    --loh case_study_output/loh_blocks_filtered.txt \
    --het case_study_output/extract_results/S_para_chrXII.exp.het_blocks.bed \
    --output-dir case_study_output \
    --prefix loh_visualization \
    --aspect-ratio 0.35 \
    --width 2000 \
    --height 750 \
    --res 250
```

**Expected output**: PNG files showing LOH propensity across the chromosome, saved in `case_study_output/plots/`.

### Step 6: Simulate Alternative Genome (Optional)

Simulate a divergent genome for comparison studies:

```bash
# Simulate a 1% divergent genome
jloh sim \
    --fasta test_data/S_para.chrXII.fa \
    --out-fasta case_study_output/S_para_chrXII_divergent.fa \
    --divergence 0.01 \
    --out-haplotypes case_study_output/simulated_haplotypes.txt
```

### Step 7: Advanced Analysis - Clustering

If you have multiple samples, cluster them by LOH similarity:

```bash
# For demonstration, create a second filtered file
cp case_study_output/loh_blocks_filtered.txt case_study_output/loh_blocks_sample2.txt

# Cluster multiple samples
jloh cluster \
    --loh case_study_output/loh_blocks_filtered.txt case_study_output/loh_blocks_sample2.txt \
    --out-prefix case_study_output/clustered_blocks \
    --max-dist 0.3
```

### Step 8: Intersect with Genomic Features (Optional)

Demonstrate intersection capabilities:

```bash
# Create a simple GFF file for demonstration
cat > case_study_output/demo_features.gff << 'EOF'
S_para_chrXII	demo	gene	1000	5000	.	+	.	ID=gene1;Name=example_gene1
S_para_chrXII	demo	gene	10000	15000	.	-	.	ID=gene2;Name=example_gene2
S_para_chrXII	demo	gene	50000	55000	.	+	.	ID=gene3;Name=example_gene3
EOF

# Note: The chimeric command requires two separate haplotype files
# For single-sample analysis, we can demonstrate intersection between two LOH files
jloh intersect \
    --loh-A case_study_output/loh_blocks_filtered.txt \
    --loh-B case_study_output/loh_blocks_sample2.txt \
    --mode intersection \
    --min-ovl 0.5 \
    > case_study_output/intersect_results.txt
```

### Step 9: Genome-to-Genome Comparison (Advanced)

Compare two genomes to identify potential LOH regions:

```bash
# Create output directory for g2g results
mkdir -p case_study_output/g2g_results

# Compare original vs simulated genome (if simulation was successful)
if [ -f "case_study_output/S_para_chrXII_divergent.fa" ]; then
    jloh g2g \
        --ref-A test_data/S_para.chrXII.fa \
        --ref-B case_study_output/S_para_chrXII_divergent.fa \
        --output-dir case_study_output/g2g_results
    echo "G2G comparison completed. Results in case_study_output/g2g_results/"
else
    echo "Simulated genome not found. Run Step 6 first."
fi
```

### Step 10: Oncology-Specific Analysis (Optional)

**Note**: The onco_extract command currently has a bug in single-mode. This step is disabled.

```bash
# Note: onco_extract has a parameter bug in the current version
# Typical usage would be for tumor/normal pairs:
echo "onco_extract step skipped due to parameter handling bug"
echo "This command is typically used with tumor/normal sample pairs"

# Example of what the command would look like when fixed:
# jloh onco_extract \
#     --vcfs control.vcf tumor.vcf \
#     --bams control.bam tumor.bam \
#     --ref reference.fa \
#     --sample "tumor_sample" \
#     --output-dir onco_results
```

## Complete Pipeline Script

Here's a complete bash script that runs the working parts of the pipeline using the CLI:

```bash
#!/bin/bash
# complete_pipeline.sh - Full JLOH analysis pipeline using CLI

set -e  # Exit on any error

echo "🧬 Starting JLOH Pipeline Analysis"
echo "=================================="

# Activate environment ONCE
conda activate jloh

# Install package if needed
pip install -e . > /dev/null 2>&1

# Create output directory
mkdir -p case_study_output
cd case_study_output

echo "📊 Step 1: SNP Statistics..."
jloh stats \
    --vcf ../test_data/out.ff.vcf \
    --threads 2 \
    > snp_stats.txt

echo "🔍 Step 2: Extract LOH Blocks..."
jloh extract \
    --vcf ../test_data/out.ff.vcf \
    --bam ../test_data/out.fs.bam \
    --ref ../test_data/S_para.chrXII.fa \
    --sample "S_para_chrXII" \
    --output-dir extract_results \
    --min-length 100 \
    --min-snps-kbp 1,0.5 \
    --threads 2

# Copy results to standard filename
cp extract_results/S_para_chrXII.LOH_blocks.tsv loh_blocks.txt

echo "🔬 Step 3: Filter LOH Blocks..."
jloh filter \
    --loh loh_blocks.txt \
    --length 500 \
    --snps 3 \
    --coverage 5 \
    > loh_blocks_filtered.txt

echo "🔗 Step 4: Analyze Junctions..."
jloh junctions \
    --blocks loh_blocks_filtered.txt \
    --max-dist 5000 \
    --genome ../test_data/S_para.chrXII.fa \
    > junction_stats.txt

echo "📈 Step 5: Create Visualization..."
jloh plot \
    --one-ref \
    --loh loh_blocks_filtered.txt \
    --het extract_results/S_para_chrXII.exp.het_blocks.bed \
    --output-dir . \
    --prefix loh_visualization \
    --aspect-ratio 0.35 \
    --width 2000 \
    --height 750 \
    --res 250

echo "🧪 Step 6: Simulate Divergent Genome..."
jloh sim \
    --fasta ../test_data/S_para.chrXII.fa \
    --out-fasta S_para_chrXII_divergent.fa \
    --divergence 0.01 \
    --out-haplotypes simulated_haplotypes.txt

echo "📊 Step 7: Clustering Analysis..."
# Create demo sample for clustering
cp loh_blocks_filtered.txt loh_blocks_sample2.txt

jloh cluster \
    --loh loh_blocks_filtered.txt loh_blocks_sample2.txt \
    --out-prefix clustered_blocks \
    --max-dist 0.3

echo "🔗 Step 8: Intersection Analysis..."
# Create demo GFF
cat > demo_features.gff << 'EOF'
S_para_chrXII	demo	gene	1000	5000	.	+	.	ID=gene1;Name=example_gene1
S_para_chrXII	demo	gene	10000	15000	.	-	.	ID=gene2;Name=example_gene2
S_para_chrXII	demo	gene	50000	55000	.	+	.	ID=gene3;Name=example_gene3
EOF

# Intersection analysis between LOH files
jloh intersect \
    --loh-A loh_blocks_filtered.txt \
    --loh-B loh_blocks_sample2.txt \
    --mode intersection \
    --min-ovl 0.5 \
    > intersect_results.txt

echo "🧬 Step 9: Genome-to-Genome Analysis..."
mkdir -p g2g_results
if [ -f "S_para_chrXII_divergent.fa" ]; then
    jloh g2g \
        --ref-A ../test_data/S_para.chrXII.fa \
        --ref-B S_para_chrXII_divergent.fa \
        --output-dir g2g_results
fi

echo "⚠️  Step 10: Oncology analysis (Skipped - parameter bug)"

echo "✅ Pipeline completed successfully!"
echo "📁 Results saved in: case_study_output/"
echo ""
echo "Key output files:"
echo "  - snp_stats.txt           : SNP statistics"
echo "  - loh_blocks.txt          : Raw LOH blocks"
echo "  - loh_blocks_filtered.txt : Filtered LOH blocks"
echo "  - junction_stats.txt      : Junction analysis"
echo "  - S_para_chrXII_divergent.fa : Simulated genome"
echo "  - clustered_blocks.*.tsv  : Clustering results"
echo "  - intersect_results.txt   : Intersection analysis"
echo "  - g2g_results/            : Genome comparison"
echo ""
echo "⚠️  Note: Some features skipped due to current CLI limitations:"
echo "   - Plot visualization (R script path issue)"
echo "   - Oncology analysis (parameter bug)"
```

## Expected Results

After running the pipeline, you should have:

1. **SNP Statistics** (`snp_stats.txt`): Summary of variant properties
2. **LOH Blocks** (`loh_blocks_filtered.txt`): Filtered regions of loss of heterozygosity
3. **Junction Analysis** (`junction_stats.txt`): Statistics on block boundaries
4. **Visualization** (`loh_plot.png`): Graphical representation of LOH landscape
5. **Simulated Data** (`S_para_chrXII_divergent.fa`): Alternative genome for comparisons

## Interpretation Guide

### Understanding LOH Blocks

LOH blocks in the output represent genomic regions where:
- **REF blocks**: Regions matching the reference allele
- **ALT blocks**: Regions with alternative alleles
- **Length**: Physical size of the block
- **SNPs**: Number of supporting variants
- **Coverage**: Sequencing depth

### Quality Metrics

- **High-confidence blocks**: Length > 1000 bp, SNPs > 5, Coverage > 10x
- **Junction density**: Number of transitions per kb
- **Allelic balance**: Ratio of REF to ALT blocks

## Troubleshooting

### Common Issues

1. **Memory errors**: Reduce `--threads` parameter
2. **Empty results**: Check input file formats and paths
3. **Plot generation fails**: Ensure matplotlib and seaborn are installed
4. **Permission errors**: Check write permissions in output directory

### Validation

```bash
# Check if key output files exist
ls -la case_study_output/
# Should show: loh_blocks_filtered.txt, loh_plot.png, etc.

# Verify LOH blocks format
head -5 case_study_output/loh_blocks_filtered.txt
# Should show: #Chrom, Start, End, Allele, Length, SNPs, Coverage

# Check plot was generated
file case_study_output/loh_plot.png
# Should show: PNG image data
```

## Next Steps

1. **Biological Interpretation**: Correlate LOH patterns with known genomic features
2. **Comparative Analysis**: Compare with other strains or conditions
3. **Statistical Testing**: Test for significant LOH enrichment in specific regions
4. **Integration**: Combine with other genomic datasets (RNA-seq, ChIP-seq)

## Citation

If you use JLOH in your research, please cite:
> Schiavinato, M. et al. (2023). JLOH: Inferring Loss of Heterozygosity Blocks from Short-read sequencing data. Bioinformatics.

---

*This case study demonstrates the complete JLOH workflow using realistic test data from Saccharomyces paradoxus chromosome XII.*
