"""Smoke tests for JLOH modules - test help functionality."""
import pytest
import subprocess
import sys
from pathlib import Path


class TestModuleHelp:
    """Test that all modules can display help without errors."""
    
    def setup_method(self):
        """Set up test environment."""
        self.jloh_dir = Path(__file__).parent.parent
        self.jloh_modules = [
            'stats', 'extract', 'filter', 'plot', 'sim',
            'cluster', 'chimeric', 'intersect', 'junctions', 'g2g', 'onco_extract'
        ]
    
    def run_module_help(self, module_name):
        """Run a module with --help flag."""
        cmd = [sys.executable, str(self.jloh_dir / 'jloh' / f'{module_name}.py'), '--help']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result
    
    def test_stats_help(self):
        """Test stats module help."""
        result = self.run_module_help('stats')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_extract_help(self):
        """Test extract module help."""
        result = self.run_module_help('extract')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_filter_help(self):
        """Test filter module help."""
        result = self.run_module_help('filter')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_plot_help(self):
        """Test plot module help."""
        result = self.run_module_help('plot')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_sim_help(self):
        """Test sim module help."""
        result = self.run_module_help('sim')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_cluster_help(self):
        """Test cluster module help."""
        result = self.run_module_help('cluster')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_chimeric_help(self):
        """Test chimeric module help."""
        result = self.run_module_help('chimeric')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_intersect_help(self):
        """Test intersect module help."""
        result = self.run_module_help('intersect')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_junctions_help(self):
        """Test junctions module help."""
        result = self.run_module_help('junctions')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_g2g_help(self):
        """Test g2g module help."""
        result = self.run_module_help('g2g')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()
    
    def test_onco_extract_help(self):
        """Test onco_extract module help."""
        result = self.run_module_help('onco_extract')
        assert result.returncode == 0
        assert 'usage:' in result.stderr.lower() or 'usage:' in result.stdout.lower()


class TestCLIInterface:
    """Test the CLI interface."""
    
    def setup_method(self):
        """Set up test environment."""
        self.jloh_dir = Path(__file__).parent.parent
    
    def test_cli_help(self):
        """Test main CLI help."""
        cmd = [sys.executable, str(self.jloh_dir / 'jloh' / 'cli.py'), '--help']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        assert result.returncode == 0
        assert 'JLOH' in result.stdout
        assert 'Extraction' in result.stdout
        assert 'Operations' in result.stdout
        assert 'Visualization' in result.stdout
        assert 'Simulation' in result.stdout
    
    def test_cli_no_args(self):
        """Test CLI with no arguments shows help."""
        cmd = [sys.executable, str(self.jloh_dir / 'jloh' / 'cli.py')]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        assert result.returncode == 0
        assert 'JLOH' in result.stdout
    
    def test_cli_invalid_module(self):
        """Test CLI with invalid module name."""
        cmd = [sys.executable, str(self.jloh_dir / 'jloh' / 'cli.py'), 'invalid_module']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        assert result.returncode == 1
        assert 'Error:' in result.stderr or 'not found' in result.stderr
