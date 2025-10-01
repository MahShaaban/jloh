#!/bin/bash
# run_case_study_cli_fixed.sh - JLOH Case Study Pipeline using CLI commands

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧬 Starting JLOH Case Study Pipeline (CLI Version)${NC}"
echo -e "${BLUE}=================================================${NC}"

# Check if conda environment is active
if [[ "$CONDA_DEFAULT_ENV" != "jloh" ]]; then
    echo -e "${YELLOW}⚠️  Activating JLOH conda environment${NC}"
    conda activate jloh
fi

# Install package in development mode
echo -e "${BLUE}📦 Installing JLOH package${NC}"
pip install -e . > /dev/null 2>&1

# Create output directory
mkdir -p case_study_output
cd case_study_output

echo -e "${GREEN}📊 Step 1: SNP Statistics Analysis${NC}"
jloh stats \
    --vcf ../test_data/out.ff.vcf \
    --threads 2 \
    > snp_stats.txt
echo -e "${GREEN}✓ SNP statistics saved to snp_stats.txt${NC}"

echo -e "${GREEN}🔍 Step 2: Extract LOH Blocks${NC}"
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
echo -e "${GREEN}✓ LOH blocks extracted and saved${NC}"

echo -e "${GREEN}🔬 Step 3: Filter LOH Blocks${NC}"
jloh filter \
    --loh loh_blocks.txt \
    --length 500 \
    --snps 3 \
    --coverage 5 \
    > loh_blocks_filtered.txt
echo -e "${GREEN}✓ LOH blocks filtered${NC}"

echo -e "${GREEN}🔗 Step 4: Analyze Block Junctions${NC}"
jloh junctions \
    --blocks loh_blocks_filtered.txt \
    --max-dist 5000 \
    --genome ../test_data/S_para.chrXII.fa \
    > junction_stats.txt
echo -e "${GREEN}✓ Junction analysis completed${NC}"

echo -e "${GREEN}📈 Step 5: Create Visualization${NC}"
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
echo -e "${GREEN}✓ Visualization completed${NC}"

echo -e "${GREEN}🧪 Step 6: Simulate Divergent Genome${NC}"
jloh sim \
    --fasta ../test_data/S_para.chrXII.fa \
    --out-fasta S_para_chrXII_divergent.fa \
    --divergence 0.01 \
    --out-haplotypes simulated_haplotypes.txt
echo -e "${GREEN}✓ Divergent genome simulated${NC}"

echo -e "${GREEN}📊 Step 7: Clustering Analysis${NC}"
# Create demo sample for clustering
cp loh_blocks_filtered.txt loh_blocks_sample2.txt

jloh cluster \
    --loh loh_blocks_filtered.txt loh_blocks_sample2.txt \
    --out-prefix clustered_blocks \
    --max-dist 0.3
echo -e "${GREEN}✓ Clustering analysis completed${NC}"

echo -e "${GREEN}🔗 Step 8: Intersection Analysis${NC}"
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
echo -e "${GREEN}✓ Intersection analysis completed${NC}"

echo -e "${GREEN}🧬 Step 9: Genome-to-Genome Comparison${NC}"
mkdir -p g2g_results
if [ -f "S_para_chrXII_divergent.fa" ]; then
    jloh g2g \
        --ref-A ../test_data/S_para.chrXII.fa \
        --ref-B S_para_chrXII_divergent.fa \
        --output-dir g2g_results
    echo -e "${GREEN}✓ G2G comparison completed${NC}"
else
    echo -e "${RED}✗ Simulated genome not found${NC}"
fi

echo -e "${YELLOW}⚠️  Step 10: Oncology analysis (Skipped due to parameter bug)${NC}"

cd ..

echo -e "${BLUE}✅ Pipeline completed successfully!${NC}"
echo -e "${BLUE}📁 Results saved in: case_study_output/${NC}"
echo ""
echo -e "${GREEN}Key output files:${NC}"
echo "  📊 snp_stats.txt           : SNP statistics"
echo "  🧬 loh_blocks.txt          : Raw LOH blocks"
echo "  🔬 loh_blocks_filtered.txt : Filtered LOH blocks"
echo "  🔗 junction_stats.txt      : Junction analysis"
echo "  📈 plots/                  : LOH visualization plots"
echo "  🧪 S_para_chrXII_divergent.fa : Simulated genome"
echo "  📊 clustered_blocks.*.tsv  : Clustering results"
echo "  🔗 intersect_results.txt   : Intersection analysis"
echo "  🧬 g2g_results/            : Genome comparison results"

echo ""
echo -e "${YELLOW}⚠️  Known limitations in current CLI version:${NC}"
echo "   • Chimeric gene analysis (requires two haplotype files)"
echo "   • Oncology analysis (parameter handling bug)"

# Count LOH blocks found
if [ -f "case_study_output/loh_blocks_filtered.txt" ]; then
    BLOCKS=$(tail -n +2 case_study_output/loh_blocks_filtered.txt | wc -l)
    echo ""
    echo -e "${GREEN}📈 Analysis Results Summary:${NC}"
    echo "   • LOH blocks identified: $BLOCKS"
    echo "   • Test data: Saccharomyces paradoxus chromosome XII"
    echo "   • Pipeline demonstrates JLOH's core functionality"
fi
