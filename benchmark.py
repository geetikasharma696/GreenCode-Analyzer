
import os
import sys
import time
import subprocess
import psutil


def benchmark_python_file(file_path, timeout=10):

    if not os.path.isfile(file_path):
        raise FileNotFoundError("Python file not found.")

    if not file_path.lower().endswith(".py"):
        raise ValueError("Please select a Python file.")

    print("\nStarting performance benchmark...")

    start_time = time.perf_counter()

    process = subprocess.Popen(
        [sys.executable, file_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )

    monitored_process = psutil.Process(process.pid)

    peak_memory = 0
    peak_cpu_usage = 0
    cpu_time = 0
    timed_out = False
    error_message = ""

    try:
        monitored_process.cpu_percent(interval=None)

        while process.poll() is None:

            try:
                memory_info = monitored_process.memory_info()
                peak_memory = max(peak_memory, memory_info.rss)

                current_cpu = monitored_process.cpu_percent(interval=None)
                peak_cpu_usage = max(peak_cpu_usage, current_cpu)

                cpu_info = monitored_process.cpu_times()
                cpu_time = cpu_info.user + cpu_info.system

            except psutil.NoSuchProcess:
                break

            if time.perf_counter() - start_time > timeout:
                timed_out = True
                process.kill()
                break

            time.sleep(0.02)

        _, error_message = process.communicate(timeout=2)

    except Exception:
        if process.poll() is None:
            process.kill()

        process.communicate()
        raise

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    peak_memory_mb = peak_memory / (1024 * 1024)

    average_cpu_usage = (
        (cpu_time / execution_time) * 100
        if execution_time > 0 else 0
    )

    return {
        "execution_time": execution_time,
        "cpu_time": cpu_time,
        "cpu_usage": average_cpu_usage,
        "peak_cpu_usage": peak_cpu_usage,
        "peak_memory": peak_memory_mb,
        "timed_out": timed_out,
        "return_code": process.returncode,
        "error_message": error_message.strip()
    }


if __name__ == "__main__":

    file_path = input(
        "Enter Python file path to benchmark: "
    ).strip()

    try:
        results = benchmark_python_file(file_path)

        print("\n--- GreenCode Benchmark Report ---")

        print("Execution Time:",
              round(results["execution_time"], 4), "seconds")

        print("CPU Time:",
              round(results["cpu_time"], 4), "seconds")

        print("Average CPU Usage:",
              round(results["cpu_usage"], 2), "%")

        print("Peak CPU Usage:",
              round(results["peak_cpu_usage"], 2), "%")

        print("Peak Memory:",
              round(results["peak_memory"], 2), "MB")

        if results["timed_out"]:
            print("Status: Time limit reached.")

        elif results["return_code"] == 0:
            print("Status: Execution completed successfully.")

        else:
            print("Status: Program ended with an error.")
            print("Error:", results["error_message"])

    except Exception as error:
        print("Benchmark Error:", error)
