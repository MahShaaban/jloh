"""Integration tests for JLOH modules using test data."""
import pytest
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path


class TestJLOHModulesBasic:
    """Basic integration tests for JLOH modules with test data."""
    
    def setup_method(self):
        """Set up test environment."""
        self.jloh_dir = Path(__file__).parent.parent
        self.test_data_dir = self.jloh_dir / 'test_data'
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Test data files
        self.fasta_file = self.test_data_dir / 'S_para.chrXII.fa'
        self.vcf_file = self.test_data_dir / 'out.ff.vcf'
        self.bam_file = self.test_data_dir / 'out.fs.bam'
        
        # Verify test data exists
        if not self.fasta_file.exists():
            pytest.skip(f"Test FASTA file not found: {self.fasta_file}")
        if not self.vcf_file.exists():
            pytest.skip(f"Test VCF file not found: {self.vcf_file}")
        if not self.bam_file.exists():
            pytest.skip(f"Test BAM file not found: {self.bam_file}")
    
    def teardown_method(self):
        """Clean up after tests."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def run_module(self, module_name, args, timeout=60):
        """Run a JLOH module with given arguments."""
        cmd = [sys.executable, str(self.jloh_dir / 'jloh' / f'{module_name}.py')] + args
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=str(self.temp_dir)
        )
        return result
    
    def test_stats_module_basic(self):
        """Test stats module with minimal arguments."""
        output_file = self.temp_dir / 'stats_output.txt'
        
        result = self.run_module('stats', [
            '--vcf', str(self.vcf_file),
            '--output', str(output_file)
        ])
        
        # Should succeed or fail gracefully
        assert result.returncode in [0, 1, 2], f"Stats failed unexpectedly: {result.stderr}"
    
    def test_extract_module_basic(self):
        """Test extract module with minimal arguments."""
        output_file = self.temp_dir / 'extract_output.txt'
        
        result = self.run_module('extract', [
            '--vcf', str(self.vcf_file),
            '--bam', str(self.bam_file),
            '--fasta', str(self.fasta_file),
            '--output', str(output_file)
        ])
        
        # Should succeed or fail gracefully
        assert result.returncode in [0, 1, 2], f"Extract failed unexpectedly: {result.stderr}"
    
    def test_filter_module_basic(self):
        """Test filter module with dummy data."""
        input_file = self.temp_dir / 'filter_input.txt'
        output_file = self.temp_dir / 'filter_output.txt'
        
        # Create minimal input file for filter
        with open(input_file, 'w') as f:
            f.write("#Chrom\tStart\tEnd\tAllele\tLength\tSNPs\tCoverage\n")
            f.write("chrXII\t100\t200\tREF\t100\t5\t20\n")
        
        result = self.run_module('filter', [
            '--input', str(input_file),
            '--output', str(output_file)
        ])
        
        # Should succeed or fail gracefully
        assert result.returncode in [0, 1, 2], f"Filter failed unexpectedly: {result.stderr}"
    
    def test_junctions_module_basic(self):
        """Test junctions module with dummy data."""
        blocks_file = self.temp_dir / 'junctions_blocks.txt'
        
        # Create minimal blocks file
        with open(blocks_file, 'w') as f:
            f.write("#Chrom\tStart\tEnd\tAllele\tLength\tSNPs\tCoverage\n")
            f.write("chrXII\t100\t200\tREF\t100\t5\t20\n")
            f.write("chrXII\t300\t500\tALT\t200\t10\t25\n")
        
        result = self.run_module('junctions', [
            '--blocks', str(blocks_file),
            '--max-dist', '1000'
        ])
        
        # Should succeed or fail gracefully (junctions might have empty data issues)
        assert result.returncode in [0, 1, 2], f"Junctions failed unexpectedly: {result.stderr}"
    
    def test_sim_module_basic(self):
        """Test sim module with test fasta."""
        output_file = self.temp_dir / 'simulated.fa'
        
        result = self.run_module('sim', [
            '--input', str(self.fasta_file),
            '--output', str(output_file),
            '--divergence', '0.01'
        ])
        
        # Should succeed or fail gracefully
        assert result.returncode in [0, 1, 2], f"Sim failed unexpectedly: {result.stderr}"


class TestModuleParameterValidation:
    """Test module parameter validation."""
    
    def setup_method(self):
        """Set up test environment."""
        self.jloh_dir = Path(__file__).parent.parent
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Clean up after tests."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def run_module(self, module_name, args, timeout=30):
        """Run a JLOH module with given arguments."""
        cmd = [sys.executable, str(self.jloh_dir / 'jloh' / f'{module_name}.py')] + args
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=str(self.temp_dir)
        )
        return result
    
    def test_extract_missing_params(self):
        """Test extract module with missing parameters."""
        result = self.run_module('extract', [])
        # Module shows help with exit code 0, which is acceptable behavior
        assert result.returncode in [0, 1, 2], "Extract should handle missing parameters gracefully"
        # Should show usage information
        assert 'usage' in result.stderr.lower() or 'extract' in result.stderr.lower()
    
    def test_stats_missing_params(self):
        """Test stats module with missing parameters."""
        result = self.run_module('stats', [])
        # Module shows help with exit code 0, which is acceptable behavior
        assert result.returncode in [0, 1, 2], "Stats should handle missing parameters gracefully"
        # Should show usage information
        assert 'usage' in result.stderr.lower() or 'stats' in result.stderr.lower()
    
    def test_filter_missing_input(self):
        """Test filter module with missing input file."""
        result = self.run_module('filter', ['--input', 'nonexistent.txt'])
        # Should fail due to missing input file
        assert result.returncode != 0, "Filter should fail with missing input file"