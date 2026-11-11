
import os
import sys
import subprocess


print("\n===================================")
print("       GREENCODE ANALYZER")
print("===================================")

# Ask for Python file path only once
file_path = input("\nEnter Python file path: ").strip()

# Check file existence
if not os.path.isfile(file_path):
    print("\nError: File not found.")
    raise SystemExit

if not file_path.lower().endswith(".py"):
    print("\nError: Please select a Python file.")
    raise SystemExit


# Run static analysis
print("\n===================================")
print("       STATIC CODE ANALYSIS")
print("===================================")

analysis_result = subprocess.run(
    [sys.executable, "analyzer.py"],
    input=file_path + "\n",
    text=True
)


# Run performance benchmark
print("\n===================================")
print("       PERFORMANCE BENCHMARK")
print("===================================")

benchmark_result = subprocess.run(
    [sys.executable, "benchmark.py"],
    input=file_path + "\n",
    text=True
)


# Final status
print("\n===================================")
print("       ANALYSIS COMPLETED")
print("===================================")

if analysis_result.returncode == 0 and benchmark_result.returncode == 0:
    print("GreenCode analysis workflow completed.")
else:
    print("One or more analysis modules encountered an error.")
