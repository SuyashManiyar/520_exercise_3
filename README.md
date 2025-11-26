

## Files Included

### Main Files
1. **demo_humaneval_clean.py** - Main script to run coverage analysis
2. **gemma_notebook.ipynb** - Jupyter notebook for analysis
3. **coverage_pipeline.py** - Core coverage pipeline implementation
4. **requirements.txt** - Python dependencies

### Supporting Files
- **codes/** - Directory containing Python files to analyze

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Coverage Analysis
```bash
python3 demo_humaneval_clean.py
```

### 3. Use Jupyter Notebook
```bash
jupyter notebook gemma_notebook.ipynb
```

## What You Get

When you run `demo_humaneval_clean.py`, you'll see:

```
================================================================================
RESULTS
================================================================================
Problem ID:          BASE_APPS
Tests Passed:        12/12
Tests Failed:        0/12
Statement Coverage:  71.1% (57/78 statements)
Branch Coverage:     68.0%

Interpretation:      Moderate line coverage - some untested code paths
================================================================================
HTML Report: coverage_reports/BASE_APPS/index.html
================================================================================
```

## Coverage Metrics

- **Statement Coverage**: Percentage and count of statements executed
- **Branch Coverage**: Percentage of conditional branches tested

## Customizing

Edit `demo_humaneval_clean.py` to:
- Change the Python file to analyze
- Modify test cases
- Update the problem ID

Example:
```python
result = pipeline.analyze(
    python_file="codes/your_file.py",
    test_cases=your_test_cases,
    problem_id="your_problem_id"
)
```

## Dependencies

- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- coverage >= 7.0.0

All specified in `requirements.txt`
