"""Basic import and package tests for JLOH."""
import pytest
import sys
from pathlib import Path

# Add jloh to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent))

import jloh
from jloh import cli


def test_package_version():
    """Test that package version is accessible."""
    assert hasattr(jloh, '__version__')
    assert jloh.__version__ == "1.1.0"


def test_package_metadata():
    """Test package metadata."""
    assert hasattr(jloh, '__author__')
    assert hasattr(jloh, '__email__')
    assert hasattr(jloh, '__description__')


def test_cli_import():
    """Test that CLI module can be imported."""
    assert hasattr(cli, 'main')
    assert callable(cli.main)


def test_modules_import():
    """Test that all expected modules can be imported safely."""
    import importlib.util
    
    # List of all JLOH modules
    modules = [
        'stats', 'extract', 'filter', 'plot', 'sim',
        'cluster', 'chimeric', 'intersect', 'junctions', 'g2g', 'onco_extract'
    ]
    
    jloh_dir = Path(__file__).parent.parent / 'jloh'
    
    for module_name in modules:
        module_path = jloh_dir / f"{module_name}.py"
        assert module_path.exists(), f"Module file {module_name}.py not found"
        
        # Check that the file can be read and has basic Python structure
        with open(module_path, 'r') as f:
            content = f.read()
            assert 'import' in content, f"Module {module_name} doesn't seem to have imports"
            assert 'def' in content or 'class' in content, f"Module {module_name} doesn't have functions or classes"
