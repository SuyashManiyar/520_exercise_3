# Quick Guide - Required Code Base

## 📁 What's in This Folder

```
required_code_base/
├── demo_humaneval_clean.py    # Main script - RUN THIS
├── gemma_notebook.ipynb        # Jupyter notebook
├── coverage_pipeline.py        # Core implementation
├── requirements.txt            # Dependencies
├── codes/                      # Python files to analyze
├── README.md                   # Detailed documentation
├── QUICK_GUIDE.md             # This file
└── run_analysis.sh            # Quick run script
```

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Analysis
```bash
python3 demo_humaneval_clean.py
```

OR use the script:
```bash
./run_analysis.sh
```

### Step 3: View Results
The output shows:
- Statement Coverage (% and count)
- Branch Coverage (%)
- Test results
- HTML report path

## 📊 Example Output

```
================================================================================
RESULTS
================================================================================
Problem ID:          PROMPT_UPDATED_HUMANEVAL_114
Tests Passed:        27/27
Tests Failed:        0/27
Statement Coverage:  100.0% (10/10 statements)
Branch Coverage:     100.0%

Interpretation:      Excellent coverage - well-tested code
================================================================================
HTML Report: coverage_reports/PROMPT_UPDATED_HUMANEVAL_114/index.html
================================================================================
```

## 🎯 Two Main Files

### 1. demo_humaneval_clean.py
**Purpose**: Run coverage analysis on Python files

**How to use**:
```bash
python3 demo_humaneval_clean.py
```

**What it does**:
- Analyzes Python code with test cases
- Measures statement and branch coverage
- Generates HTML reports
- Shows expected vs actual for failed tests

### 2. gemma_notebook.ipynb
**Purpose**: Interactive Jupyter notebook for analysis

**How to use**:
```bash
jupyter notebook gemma_notebook.ipynb
```

**What it does**:
- Interactive code analysis
- Visualization of results
- Experimentation with different test cases

## 🔧 Customizing the Analysis

Edit `demo_humaneval_clean.py`:

```python
# Change the file to analyze
python_file="codes/your_file.py"

# Modify test cases
test_cases = [
    "assert candidate([1, 2, 3]) == 1",
    "assert candidate([-1, -2]) == -3",
]

# Update problem ID
problem_id="your_problem_name"
```

## 📦 Dependencies

All you need:
- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- coverage >= 7.0.0

Installed with: `pip install -r requirements.txt`

## 🎓 Understanding the Output

### Statement Coverage
- Shows % of statements executed
- Shows count: `(10/10 statements)` = 10 out of 10 executed
- Goal: 80%+ is good

### Branch Coverage
- Shows % of conditional branches tested
- Includes if/else, loops, etc.
- Goal: 80%+ is good

### Interpretation
- Automatic summary of coverage quality
- Tells you what to improve

## 🔍 Viewing HTML Reports

After running, open the HTML report:
```bash
open coverage_reports/PROBLEM_ID/index.html
```

The HTML report shows:
- Line-by-line coverage (green = covered, red = not covered)
- Branch coverage details
- Exact lines that need testing

## ⚡ Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
python3 demo_humaneval_clean.py

# Or use the script
./run_analysis.sh

# Open Jupyter notebook
jupyter notebook gemma_notebook.ipynb

# View HTML report (after running)
open coverage_reports/*/index.html
```

## 💡 Tips

1. **Start Simple**: Run `demo_humaneval_clean.py` first to see how it works
2. **Check HTML Reports**: They show exactly which lines need testing
3. **Iterate**: Add test cases for uncovered lines/branches
4. **Use Jupyter**: For interactive exploration, use the notebook

## 🆘 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "File not found" error
Make sure you're in the `required_code_base` folder:
```bash
cd required_code_base
python3 demo_humaneval_clean.py
```

### Want to analyze a different file?
Edit line 30 in `demo_humaneval_clean.py`:
```python
python_file="codes/your_file.py"
```

## ✅ That's It!

Just run:
```bash
python3 demo_humaneval_clean.py
```

Everything else is automatic!
