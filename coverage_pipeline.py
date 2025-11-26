#!/usr/bin/env python3
"""
Python Coverage Pipeline
A streamlined tool for analyzing Python code coverage with pytest-cov
"""

import ast
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class CoverageResult:
    """Coverage result for a single Python file analysis"""
    problem_id: str
    tests_passed: int
    tests_failed: int
    total_tests: int
    line_coverage: float
    statement_coverage: float
    branch_coverage: Optional[float]
    statements_covered: int
    statements_total: int
    interpretation: str
    error_details: List[str]
    html_report_path: str


class PythonCoveragePipeline:
    """Pipeline for analyzing Python code coverage with pytest-cov"""
    
    def __init__(self, output_dir: str = "coverage_reports"):
        """
        Initialize the pipeline.
        
        Args:
            output_dir: Directory where HTML reports will be saved
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _extract_function_name(self, python_file: str) -> str:
        """
        Parse Python file AST to find the main function name.
        
        Args:
            python_file: Path to the Python file
            
        Returns:
            Function name or "candidate" as fallback
        """
        try:
            with open(python_file, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Return first non-private function
                    if not node.name.startswith('_'):
                        return node.name
            
            print(f"Warning: No public function found in {python_file}")
            return "candidate"
            
        except Exception as e:
            print(f"Warning: Could not parse {python_file}: {e}")
            return "candidate"

    def _create_test_file(
        self,
        python_file: str,
        test_cases: List[str],
        func_name: str,
        temp_dir: str
    ) -> str:
        """
        Generate pytest test file in temporary directory.
        
        Args:
            python_file: Path to the Python file to test
            test_cases: List of assertion strings
            func_name: Name of the function to import
            temp_dir: Temporary directory for test file
            
        Returns:
            Path to the generated test file
        """
        test_file_path = os.path.join(temp_dir, "test_coverage.py")
        
        # Get solution details
        solution_module = Path(python_file).stem
        solution_dir = str(Path(python_file).parent.absolute())
        
        # Create test file content
        test_content = f"""# Auto-generated pytest test file
import sys
sys.path.insert(0, r'{solution_dir}')

try:
    from {solution_module} import {func_name}
except ImportError as e:
    print(f"Import error: {{e}}")
    {func_name} = None

# Create alias 'candidate' to call the actual function
candidate = {func_name}

"""
        
        # Add test functions
        for i, test_case in enumerate(test_cases):
            test_code = test_case.strip()
            if not test_code.startswith('assert'):
                test_code = f"assert {test_code}"
            
            test_content += f"""def test_case_{i}():
    \"\"\"Test case {i+1}\"\"\"
    {test_code}

"""
        
        # Write test file
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        
        return test_file_path
    def _run_pytest(
        self,
        test_file: str,
        python_file: str,
        temp_dir: str
    ) -> subprocess.CompletedProcess:
        """
        Execute pytest with coverage flags.
        
        Args:
            test_file: Path to the test file
            python_file: Path to the Python file being tested
            temp_dir: Temporary directory
            
        Returns:
            CompletedProcess result
        """
        solution_module = Path(python_file).stem
        coverage_json = os.path.join(temp_dir, 'coverage.json')
        html_temp_dir = os.path.join(temp_dir, 'htmlcov')
        
        cmd = [
            'pytest',
            test_file,
            f'--cov={solution_module}',
            '--cov-branch',
            '--cov-report=term-missing',
            f'--cov-report=json:{coverage_json}',
            f'--cov-report=html:{html_temp_dir}',
            '-vv',  # Very verbose to get more details
            '--tb=short',  # Short traceback format
            '-p', 'no:warnings'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=temp_dir,
            timeout=30
        )
        
        return result

    def _parse_test_results(self, output: str, total_tests: int) -> Tuple[int, int]:
        """
        Extract pass/fail counts from pytest output.
        
        Args:
            output: Pytest stdout/stderr output
            total_tests: Total number of tests
            
        Returns:
            Tuple of (passed_count, failed_count)
        """
        passed_match = re.search(r'(\d+) passed', output)
        failed_match = re.search(r'(\d+) failed', output)
        
        passed = int(passed_match.group(1)) if passed_match else 0
        failed = int(failed_match.group(1)) if failed_match else 0
        
        # If no explicit counts and return code indicates success
        if passed == 0 and failed == 0:
            if 'passed' in output.lower():
                passed = total_tests
            else:
                failed = total_tests
        
        return passed, failed

    def _parse_coverage_json(
        self,
        coverage_json_path: str,
        python_file: str
    ) -> Tuple[float, float, Optional[float], int, int]:
        """
        Extract line, statement, and branch coverage from JSON report.
        
        Args:
            coverage_json_path: Path to coverage JSON file
            python_file: Path to the Python file being analyzed
            
        Returns:
            Tuple of (line_coverage, statement_coverage, branch_coverage, statements_covered, statements_total)
        """
        try:
            if not os.path.exists(coverage_json_path):
                return 0.0, 0.0, None, 0, 0
            
            with open(coverage_json_path, 'r') as f:
                cov_data = json.load(f)
            
            # Find the solution file in coverage data
            solution_file = Path(python_file).name
            solution_abs = str(Path(python_file).resolve())
            
            file_data = None
            for file_path, data in cov_data.get('files', {}).items():
                if solution_file in file_path or file_path == solution_abs:
                    file_data = data
                    break
            
            if file_data:
                summary = file_data.get('summary', {})
                
                # Line coverage (percentage)
                line_cov = summary.get('percent_covered', 0.0)
                
                # Statement coverage (same as line coverage in Python, but with counts)
                num_statements = summary.get('num_statements', 0)
                covered_lines = summary.get('covered_lines', 0)
                statement_cov = line_cov  # In Python, statements = executable lines
                
                # Branch coverage
                branch_cov = None
                if 'num_branches' in summary and summary['num_branches'] > 0:
                    covered_branches = summary.get('covered_branches', 0)
                    total_branches = summary.get('num_branches', 0)
                    if total_branches > 0:
                        branch_cov = (covered_branches / total_branches) * 100
                
                return line_cov, statement_cov, branch_cov, covered_lines, num_statements
            
            return 0.0, 0.0, None, 0, 0
            
        except Exception as e:
            print(f"Warning: Could not parse coverage: {e}")
            return 0.0, 0.0, None, 0, 0

    def _save_html_report(
        self,
        html_temp_dir: str,
        problem_id: str
    ) -> str:
        """
        Copy HTML report to organized output directory.
        
        Args:
            html_temp_dir: Temporary directory with HTML report
            problem_id: Identifier for this analysis
            
        Returns:
            Path to saved HTML report
        """
        try:
            target_dir = os.path.join(self.output_dir, problem_id)
            
            # Copy HTML report
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            shutil.copytree(html_temp_dir, target_dir)
            
            return os.path.join(target_dir, 'index.html')
            
        except Exception as e:
            print(f"Warning: Could not save HTML report: {e}")
            return ""

    def _generate_interpretation(
        self,
        passed: int,
        failed: int,
        line_cov: float,
        branch_cov: Optional[float]
    ) -> str:
        """
        Generate human-readable coverage interpretation.
        
        Args:
            passed: Number of passed tests
            failed: Number of failed tests
            line_cov: Line coverage percentage
            branch_cov: Branch coverage percentage or None
            
        Returns:
            Human-readable interpretation string
        """
        if failed > 0:
            return f"{failed} test(s) failed - fix failing tests first"
        
        if line_cov < 50:
            return "Low line coverage - significant untested code paths"
        elif line_cov < 80:
            return "Moderate line coverage - some untested code paths"
        
        if branch_cov is not None:
            if branch_cov < 50:
                return "Low branch coverage - untested conditional logic and error paths"
            elif branch_cov < 80:
                return "Moderate branch coverage - some conditional branches untested"
        
        if line_cov >= 90:
            if branch_cov and branch_cov >= 90:
                return "Excellent coverage - well-tested code"
            elif branch_cov:
                return "Good line coverage but some branches untested"
            else:
                return "Good line coverage achieved"
        
        return "Adequate coverage"

    def _extract_errors(self, output: str) -> List[str]:
        """
        Extract error messages from pytest output with expected vs actual values.
        
        Args:
            output: Pytest stdout/stderr output
            
        Returns:
            List of error messages with details
        """
        errors = []
        lines = output.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Look for FAILED test lines
            if 'FAILED' in line and 'test_case_' in line:
                # Extract test case number
                test_match = re.search(r'test_case_(\d+)', line)
                test_num = int(test_match.group(1)) + 1 if test_match else '?'
                
                errors.append(f"\n❌ Test Case {test_num} FAILED")
                
                # Look for the assertion in the next lines
                found_assertion = False
                for j in range(i + 1, min(i + 30, len(lines))):
                    check_line = lines[j].strip()
                    
                    # Look for assertion with comparison
                    if 'assert' in check_line.lower() and any(op in check_line for op in ['==', '!=', '>', '<', '>=', '<=']):
                        # Clean up the line
                        if check_line.startswith('E '):
                            check_line = check_line[2:].strip()
                        if check_line.startswith('>'):
                            check_line = check_line[1:].strip()
                        
                        # Parse the assertion
                        if '==' in check_line:
                            # Try to extract the comparison
                            match = re.search(r'assert\s+(.+?)\s*==\s*(.+?)(?:\s|$)', check_line)
                            if match:
                                actual_expr = match.group(1).strip()
                                expected_val = match.group(2).strip()
                                
                                errors.append(f"   Expression: {actual_expr}")
                                errors.append(f"   Expected: {expected_val}")
                                
                                # Try to find the actual value in subsequent lines
                                for k in range(j + 1, min(j + 5, len(lines))):
                                    next_line = lines[k].strip()
                                    # Look for "where" or direct value comparisons
                                    if next_line.startswith('where') or '=' in next_line:
                                        if not next_line.startswith('assert'):
                                            errors.append(f"   {next_line}")
                                
                                found_assertion = True
                                break
                        else:
                            # Just show the assertion as-is
                            errors.append(f"   {check_line}")
                            found_assertion = True
                            break
                
                if not found_assertion:
                    errors.append(f"   (See full output for details)")
                
                if len(errors) >= 20:  # Limit total errors
                    break
            
            i += 1
        
        # If no detailed errors found, fall back to simple extraction
        if not errors:
            for line in lines:
                if 'FAILED' in line or 'AssertionError' in line or 'ERROR' in line:
                    errors.append(line.strip())
                    if len(errors) >= 5:
                        break
        
        return errors

    def analyze(
        self,
        python_file: str,
        test_cases: List[str],
        problem_id: str = "analysis"
    ) -> CoverageResult:
        """
        Analyze a Python file with given test cases.
        
        Args:
            python_file: Path to the Python file to analyze
            test_cases: List of assertion strings (e.g., "assert func(1) == 2")
            problem_id: Identifier for this analysis (used in reports)
        
        Returns:
            CoverageResult with all metrics and report paths
        """
        temp_dir = tempfile.mkdtemp(prefix='pytest_cov_')
        
        try:
            # Validate file exists
            if not os.path.exists(python_file):
                return CoverageResult(
                    problem_id=problem_id,
                    tests_passed=0,
                    tests_failed=len(test_cases),
                    total_tests=len(test_cases),
                    line_coverage=0.0,
                    statement_coverage=0.0,
                    branch_coverage=None,
                    statements_covered=0,
                    statements_total=0,
                    interpretation="Error: Python file not found",
                    error_details=[f"File not found: {python_file}"],
                    html_report_path=""
                )
            
            # Extract function name
            func_name = self._extract_function_name(python_file)
            
            # Create test file
            test_file = self._create_test_file(
                python_file,
                test_cases,
                func_name,
                temp_dir
            )
            
            # Run pytest
            result = self._run_pytest(test_file, python_file, temp_dir)
            
            # Parse results
            tests_passed, tests_failed = self._parse_test_results(
                result.stdout + result.stderr,
                len(test_cases)
            )
            
            # Parse coverage
            coverage_json = os.path.join(temp_dir, 'coverage.json')
            line_cov, statement_cov, branch_cov, stmts_covered, stmts_total = self._parse_coverage_json(
                coverage_json,
                python_file
            )
            
            # Save HTML report
            html_temp_dir = os.path.join(temp_dir, 'htmlcov')
            html_report_path = ""
            if os.path.exists(html_temp_dir):
                html_report_path = self._save_html_report(
                    html_temp_dir,
                    problem_id
                )
            
            # Generate interpretation
            interpretation = self._generate_interpretation(
                tests_passed,
                tests_failed,
                line_cov,
                branch_cov
            )
            
            # Extract errors
            error_details = self._extract_errors(result.stdout + result.stderr)
            
            return CoverageResult(
                problem_id=problem_id,
                tests_passed=tests_passed,
                tests_failed=tests_failed,
                total_tests=len(test_cases),
                line_coverage=line_cov,
                statement_coverage=statement_cov,
                branch_coverage=branch_cov,
                statements_covered=stmts_covered,
                statements_total=stmts_total,
                interpretation=interpretation,
                error_details=error_details,
                html_report_path=html_report_path
            )
            
        except subprocess.TimeoutExpired:
            return CoverageResult(
                problem_id=problem_id,
                tests_passed=0,
                tests_failed=len(test_cases),
                total_tests=len(test_cases),
                line_coverage=0.0,
                statement_coverage=0.0,
                branch_coverage=None,
                statements_covered=0,
                statements_total=0,
                interpretation="Timeout - execution exceeded 30 seconds",
                error_details=["Timeout"],
                html_report_path=""
            )
            
        except Exception as e:
            return CoverageResult(
                problem_id=problem_id,
                tests_passed=0,
                tests_failed=len(test_cases),
                total_tests=len(test_cases),
                line_coverage=0.0,
                statement_coverage=0.0,
                branch_coverage=None,
                statements_covered=0,
                statements_total=0,
                interpretation=f"Error: {str(e)}",
                error_details=[str(e)],
                html_report_path=""
            )
            
        finally:
            # Cleanup
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
