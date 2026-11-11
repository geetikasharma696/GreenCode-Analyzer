
import os
import time
import statistics

from codecarbon import EmissionsTracker, OutputMethod


# ORIGINAL APPROACH: Nested loops
def original_approach(data):
    duplicates = []

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j]:
                if data[i] not in duplicates:
                    duplicates.append(data[i])

    return sorted(duplicates)


# OPTIMIZED APPROACH: Set-based lookup
def optimized_approach(data):
    seen = set()
    duplicates = set()

    for number in data:
        if number in seen:
            duplicates.add(number)
        else:
            seen.add(number)

    return sorted(duplicates)


# MEASURE PERFORMANCE AND ENERGY
def measure_approach(name, function, numbers, output_file):

    os.makedirs("reports", exist_ok=True)

    tracker = EmissionsTracker(
        project_name="GreenCodeAnalyzer",
        experiment_name=name,
        tracking_mode="process",
        measure_power_secs=1,
        output_dir="reports",
        output_file=output_file,
        output_methods=[OutputMethod.CSV],
        log_level="error"
    )

    started = False
    execution_times = []
    result = None

    try:
        tracker.start()
        started = True

        # Run the same workload five times
        for _ in range(5):

            start_time = time.perf_counter()

            result = function(numbers)

            end_time = time.perf_counter()

            execution_times.append(end_time - start_time)

        emissions = tracker.stop()
        started = False

        energy_data = tracker.final_emissions_data

        # Median gives a more robust timing summary
        median_time = statistics.median(execution_times)

        # Average estimated energy and emissions per run
        average_energy = energy_data.energy_consumed / 5
        average_emissions = emissions / 5

        return {
            "name": name,
            "result": result,
            "time": median_time,
            "all_times": execution_times,
            "energy": average_energy,
            "emissions": average_emissions
        }

    finally:
        if started:
            tracker.stop()


# MAIN COMPARISON
def run_comparison():

    numbers = list(range(4000)) + list(range(4000))

    original = measure_approach(
        "Original Nested Loop",
        original_approach,
        numbers,
        "original_emissions.csv"
    )

    optimized = measure_approach(
        "Optimized Set",
        optimized_approach,
        numbers,
        "optimized_emissions.csv"
    )

    results_match = (
        original["result"] == optimized["result"]
    )

    energy_reduction = None

    if original["energy"] > 0:
        energy_reduction = (
            (original["energy"] - optimized["energy"])
            / original["energy"]
        ) * 100

    emission_reduction = None

    if original["emissions"] > 0:
        emission_reduction = (
            (original["emissions"] - optimized["emissions"])
            / original["emissions"]
        ) * 100

    return {
        "original": original,
        "optimized": optimized,
        "results_match": results_match,
        "energy_reduction": energy_reduction,
        "emission_reduction": emission_reduction
    }


if __name__ == "__main__":

    comparison = run_comparison()

    print("\n===== OPTIMIZATION IMPACT REPORT =====")

    print("\nResults Match:", comparison["results_match"])

    for key in ("original", "optimized"):

        item = comparison[key]

        print("\n", item["name"])

        print(
            "Median Execution Time:",
            round(item["time"], 6),
            "seconds"
        )

        print(
            "Average Estimated Energy:",
            item["energy"],
            "kWh per run"
        )

        print(
            "Average Estimated CO2:",
            item["emissions"],
            "kg CO2e per run"
        )

        print(
            "Individual Run Times:",
            [round(value, 6) for value in item["all_times"]]
        )

    print(
        "\nEstimated Energy Reduction:",
        comparison["energy_reduction"]
    )

    print(
        "Estimated CO2 Reduction:",
        comparison["emission_reduction"]
    )

    print(
        "\nNote: Energy and CO2 values are model-based estimates, "
        "not direct electricity-meter readings."
    )
