
import os
import sys
import time
import subprocess

from codecarbon import EmissionsTracker, OutputMethod


def monitor_python_file(file_path):

    if not os.path.isfile(file_path):
        print("Error: File not found.")
        return

    if not file_path.lower().endswith(".py"):
        print("Error: Please select a Python file.")
        return

    os.makedirs("reports", exist_ok=True)

    tracker = EmissionsTracker(
        project_name="GreenCodeAnalyzer",
        experiment_name="Selected Python File",
        tracking_mode="machine",
        measure_power_secs=1,
        output_dir="reports",
        output_file="selected_file_energy.csv",
        output_methods=[OutputMethod.CSV],
        log_level="error"
    )

    print("\nStarting energy monitoring...")
    print("Selected file:", os.path.abspath(file_path))

    start_time = time.perf_counter()

    try:
        tracker.start()

        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

    except subprocess.TimeoutExpired:
        print("\nError: Program exceeded 30 seconds.")

    except Exception as error:
        print("\nExecution error:", error)

    else:
        print("\nProgram Output:")
        print(result.stdout)

        if result.returncode == 0:
            print("Program Status: Successful")
        else:
            print("Program Status: Failed")
            print("Error Details:", result.stderr)

    finally:
        emissions_kg = tracker.stop()

    duration = time.perf_counter() - start_time
    data = tracker.final_emissions_data

    print("\n===== PYTHON FILE ENERGY REPORT =====")

    print("Execution Duration:", round(duration, 2), "seconds")
    print("Estimated Energy:", data.energy_consumed, "kWh")
    print("Estimated CO2:", emissions_kg, "kg CO2eq")

    print("\nReport saved at:")
    print("reports/selected_file_energy.csv")


if __name__ == "__main__":

    file_path = input(
        "Enter Python file path to monitor: "
    ).strip().strip('"')

    monitor_python_file(file_path)
