
def calculate_process_carbon_reduction(process_data):

    if not process_data:
        raise ValueError("Please provide process carbon data.")

    results = {}
    total_before = 0
    total_after = 0

    for process, data in process_data.items():

        electricity = data["electricity_kwh"]
        fuel = data["fuel_gj"]
        electricity_factor = data["electricity_factor"]
        fuel_factor = data["fuel_factor"]
        improvement = data["improvement_percent"]

        if min(
            electricity,
            fuel,
            electricity_factor,
            fuel_factor
        ) < 0:
            raise ValueError("Energy and emission factors cannot be negative.")

        if not 0 <= improvement <= 100:
            raise ValueError("Improvement must be between 0 and 100.")

        # Calculate baseline carbon emissions
        electricity_emissions = electricity * electricity_factor
        fuel_emissions = fuel * fuel_factor

        baseline_emissions = (
            electricity_emissions + fuel_emissions
        )

        # Simulate emissions after improvement
        emissions_saved = (
            baseline_emissions * improvement / 100
        )

        optimized_emissions = (
            baseline_emissions - emissions_saved
        )

        results[process] = {
            "before_kg": baseline_emissions,
            "after_kg": optimized_emissions,
            "saved_kg": emissions_saved,
            "improvement_percent": improvement
        }

        total_before += baseline_emissions
        total_after += optimized_emissions

    total_saved = total_before - total_after

    return {
        "process_results": results,
        "total_before_kg": total_before,
        "total_after_kg": total_after,
        "total_saved_kg": total_saved,
        "total_saved_tonnes": total_saved / 1000,
        "reduction_percent": (
            total_saved / total_before * 100
            if total_before > 0 else 0
        )
    }

if __name__ == "__main__":

    sample_data = {
        "Furnace": {
            "electricity_kwh": 1000,
            "fuel_gj": 100,
            "electricity_factor": 0.7,
            "fuel_factor": 56.1,
            "improvement_percent": 10
        },
        "Rolling Mill": {
            "electricity_kwh": 800,
            "fuel_gj": 50,
            "electricity_factor": 0.7,
            "fuel_factor": 56.1,
            "improvement_percent": 8
        }
    }

    results = calculate_process_carbon_reduction(sample_data)

    print("\n===== INDUSTRIAL CARBON REDUCTION REPORT =====")

    for process, details in results["process_results"].items():
        print(f"\nProcess: {process}")
        print(f"Before: {details['before_kg']:.2f} kg CO2")
        print(f"After: {details['after_kg']:.2f} kg CO2")
        print(f"Saved: {details['saved_kg']:.2f} kg CO2")

    print("\nTotal Before:", results["total_before_kg"], "kg CO2")
    print("Total After:", results["total_after_kg"], "kg CO2")
    print("Total Saved:", results["total_saved_kg"], "kg CO2")
    print("Reduction:", results["reduction_percent"], "%")
