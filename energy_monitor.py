
import os
import time

from codecarbon import EmissionsTracker, OutputMethod


def run_test_workload(duration_seconds=20):
    """
    Runs a controlled CPU workload for energy monitoring.
    """

    total = 0
    start_time = time.perf_counter()

    while time.perf_counter() - start_time < duration_seconds:
        for number in range(100_000):
            total += number * number

    return total


def monitor_energy():

    os.makedirs("reports", exist_ok=True)

    tracker = EmissionsTracker(
        project_name="GreenCodeAnalyzer",
        experiment_name="Energy Monitoring Test",
        tracking_mode="process",
        measure_power_secs=1,
        output_dir="reports",
        output_file="energy_emissions.csv",
        output_methods=[OutputMethod.CSV],
        log_level="error"
    )

    print("\nStarting energy monitoring...")

    try:
        tracker.start()

        result = run_test_workload(20)

    finally:
        emissions_kg = tracker.stop()

    data = tracker.final_emissions_data

    energy_kwh = data.energy_consumed

    print("\n===== ENERGY MONITORING REPORT =====")

    print("Test completed successfully.")

    print("Workload result:", result)

    print("Execution Duration:", round(data.duration, 2), "seconds")

    print("Energy Consumed:", energy_kwh, "kWh")

    print("CO2 Emissions:", emissions_kg, "kg CO2eq")

    print("CPU Energy:", data.cpu_energy, "kWh")

    print("RAM Energy:", data.ram_energy, "kWh")

    print("\nDetailed CSV report saved in:")
    print("reports/energy_emissions.csv")


if __name__ == "__main__":
    monitor_energy()
