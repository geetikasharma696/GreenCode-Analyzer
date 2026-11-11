
import os
import time
from codecarbon import EmissionsTracker, OutputMethod


def run_test_workload(duration_seconds=10):
    total = 0
    start_time = time.perf_counter()

    while time.perf_counter() - start_time < duration_seconds:
        for number in range(100_000):
            total += number * number

    return total


def measure_energy():
    os.makedirs("reports", exist_ok=True)

    tracker = EmissionsTracker(
        project_name="GreenCodeAnalyzer",
        experiment_name="Dashboard Energy Test",
        tracking_mode="process",
        measure_power_secs=1,
        output_dir="reports",
        output_file="dashboard_energy.csv",
        output_methods=[OutputMethod.CSV],
        log_level="error"
    )

    started = False

    try:
        tracker.start()
        started = True

        result = run_test_workload(10)
        emissions = tracker.stop()
        started = False

        data = tracker.final_emissions_data

        return {
            "duration": data.duration,
            "energy": data.energy_consumed,
            "co2": emissions,
            "cpu_energy": data.cpu_energy,
            "ram_energy": data.ram_energy,
            "workload_result": result
        }

    finally:
        if started:
            tracker.stop()
