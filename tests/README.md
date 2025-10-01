# JLOH Test Suite

This directory contains comprehensive tests for the JLOH package.

## Test Organization

### 1. Basic Tests (`test_basic.py`)
- **Purpose**: Package integrity and import tests
- **Coverage**: Package metadata, version, CLI import, module file existence
- **Runtime**: ~0.1 seconds
- **Tests**: 4 tests

### 2. Smoke Tests (`test_smoke.py`)
- **Purpose**: Help functionality and command-line interface
- **Coverage**: All 11 modules help output, CLI interface behavior
- **Runtime**: ~7 seconds
- **Tests**: 14 tests

### 3. Integration Tests (`test_modules.py`)
- **Purpose**: Real functionality with test data
- **Coverage**: Module execution with actual/dummy data, parameter validation
- **Runtime**: ~5 seconds
- **Tests**: 8 tests

## Running Tests

### Prerequisites
```bash
# Activate the conda environment
conda activate jloh
```

### Test Commands
```bash
# Run basic tests only (fastest)
python run_tests.py basic

# Run smoke tests only (help functionality)
python run_tests.py smoke

# Run integration tests only (real data)
python run_tests.py integration

# Run quick tests (basic + smoke, skip integration)
python run_tests.py quick

# Run all tests (comprehensive)
python run_tests.py all
```

### Direct pytest Commands
```bash
# Run specific test file
pytest tests/test_basic.py -v

# Run with coverage
pytest --cov=jloh tests/

# Run in parallel
pytest -n auto tests/
```

## Test Coverage

### Modules Tested
- ✅ **stats**: SNP statistics calculation
- ✅ **extract**: LOH block extraction
- ✅ **filter**: Block filtering
- ✅ **plot**: Visualization
- ✅ **sim**: Genome simulation
- ✅ **cluster**: Block clustering
- ✅ **chimeric**: Chimeric gene detection
- ✅ **intersect**: Block intersection
- ✅ **junctions**: Junction analysis
- ✅ **g2g**: Genome-to-genome alignment
- ✅ **onco_extract**: Oncology-specific extraction

### Test Types
- **Import Safety**: Modules can be accessed without argument parsing errors
- **Help Display**: All modules show proper help/usage information
- **Parameter Validation**: Modules handle missing/invalid parameters gracefully
- **Basic Functionality**: Core operations work with test data
- **CLI Interface**: Command-line dispatcher works correctly

## Test Data

Test data is located in `../test_data/`:
- `S_para.chrXII.fa`: Test reference genome (chromosome XII)
- `out.ff.vcf`: Test VCF file with variants
- `out.fs.bam`: Test BAM file with alignments
- `out.fs.bam.bai`: BAM index file

## Configuration

- **pytest.ini**: Test configuration and markers
- **requirements.txt**: Testing dependencies
- **Timeout**: Tests have appropriate timeouts (30-60 seconds)
- **Cleanup**: Temporary files are cleaned up after each test

## Success Criteria

A successful test run should show:
- **Basic Tests**: 4/4 passed
- **Smoke Tests**: 14/14 passed  
- **Integration Tests**: 8/8 passed
- **Total**: 26/26 tests passed

## Troubleshooting

### Common Issues
1. **Missing conda environment**: Run `conda activate jloh`
2. **Missing pytest**: Install with `conda install pytest`
3. **Missing test data**: Ensure `test_data/` directory exists
4. **Permission errors**: Check file permissions in test directory

### Dependencies
The test suite requires:
- Python 3.9+
- pytest
- All JLOH dependencies (via conda environment)
- Access to test data files
