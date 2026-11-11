
# GreenCode Analyzer
# Before vs After Industrial Sustainability Simulation


def simulate_process_improvements(process_data, improvement_percentages):

    if not process_data:
        raise ValueError("Process energy data is required.")

    if set(process_data) != set(improvement_percentages):
        raise ValueError(
            "Every process must have an improvement percentage."
        )

    results = {}
    total_before = 0
    total_after = 0

    for process, energy_before in process_data.items():

        improvement = improvement_percentages[process]

        if energy_before < 0:
            raise ValueError("Energy cannot be negative.")

        if not 0 <= improvement <= 100:
            raise ValueError(
                f"Invalid improvement percentage for {process}."
            )

        energy_saved = energy_before * improvement / 100
        energy_after = energy_before - energy_saved

        results[process] = {
            "before_gj": energy_before,
            "improvement_percent": improvement,
            "energy_saved_gj": energy_saved,
            "after_gj": energy_after
        }

        total_before += energy_before
        total_after += energy_after

    total_saved = total_before - total_after

    overall_reduction = (
        (total_saved / total_before) * 100
        if total_before > 0 else 0
    )

    return {
        "process_results": results,
        "total_before_gj": total_before,
        "total_after_gj": total_after,
        "total_saved_gj": total_saved,
        "overall_reduction_percent": overall_reduction
    }
