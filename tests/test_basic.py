"""Basic tests for JLOH package."""
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


def test_modules_exist():
    """Test that all expected modules exist."""
    from jloh import stats, extract, filter, plot, sim
    from jloh import cluster, chimeric, intersect, junctions, g2g, onco_extract
    
    # Check modules are accessible
    assert stats is not None
    assert extract is not None
    assert filter is not None
    assert plot is not None
    assert sim is not None
    assert cluster is not None
    assert chimeric is not None
    assert intersect is not None
    assert junctions is not None
    assert g2g is not None
    assert onco_extract is not None
