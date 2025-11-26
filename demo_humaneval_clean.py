from coverage_pipeline import PythonCoveragePipeline
base_test_cases = [
   "assert candidate([2, 3, 4, 1, 2, 4]) == 1",
   "assert candidate([-1, -2, -3]) == -6",
   "assert candidate([-1, -2, -3, 2, -10]) == -14",
   "assert candidate([-9999999999999999]) == -9999999999999999",
   "assert candidate([0, 10, 20, 1000000]) == 0",
   "assert candidate([-1, -2, -3, 10, -5]) == -6",
   "assert candidate([100, -1, -2, -3, 10, -5]) == -6",
   "assert candidate([10, 11, 13, 8, 3, 4]) == 3",
   "assert candidate([100, -33, 32, -1, 0, -2]) == -33",
   "assert candidate([-10]) == -10",
   "assert candidate([7]) == 7",
   "assert candidate([1, -1]) == -1"
]


new_test_cases = [
    "assert minSubArraySum([]) == 0",
    "assert minSubArraySum([1, 2, 3]) == 1",
    "assert minSubArraySum([-1, -2, -3]) == -6",
    "assert minSubArraySum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == -5",
    "assert minSubArraySum([1]) == 1",
    "assert minSubArraySum([-1]) == -1",
    "assert minSubArraySum([2, -1, 2]) == -1",
    "assert minSubArraySum([-2, -3, 4, -1, -2, 1, 5, -3]) == -5",
    "assert minSubArraySum([0, 0, 0]) == 0",
    "assert minSubArraySum([-1, 0, -2]) == -3",
    "assert minSubArraySum([1, -1, 1, -1]) == -1",
    "assert minSubArraySum([-1, -1, -1]) == -3",
    "assert minSubArraySum([1, 2, -3, 4, -5]) == -5",
    "assert minSubArraySum([-4, -3, -2, -1]) == -10",
    "assert minSubArraySum([5, 4, -1, 7, 8]) == -1",
]


test_cases=base_test_cases+new_test_cases



pipeline = PythonCoveragePipeline(output_dir="coverage_reports")


result = pipeline.analyze(
    python_file="/Users/suyashmaniyar/Desktop/UMass/Courses/SoftwareEngineering/520_exercise_3/codes/gemma_Self_Planning/HumanEval_114.py",
    test_cases=test_cases,
    problem_id="PROMPT_UPDATED_HUMANEVAL_114"
)

# Display results
print("=" * 80)
print("RESULTS")
print("=" * 80)
print(f"Problem ID:          {result.problem_id}")
print(f"Tests Passed:        {result.tests_passed}/{result.total_tests}")
print(f"Tests Failed:        {result.tests_failed}/{result.total_tests}")
print(f"Statement Coverage:  {result.statement_coverage:.1f}% ({result.statements_covered}/{result.statements_total} statements)")
print(f"Branch Coverage:     {result.branch_coverage:.1f}%")
print(f"\nInterpretation:      {result.interpretation}")

if result.error_details:
    print("\n" + "=" * 80)
    print("FAILED TESTS - Expected vs Actual")
    print("=" * 80)
    
    for error in result.error_details:
        print(error)
    
    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)


print("=" * 80)
print(f"HTML Report: {result.html_report_path}")
print("=" * 80)
