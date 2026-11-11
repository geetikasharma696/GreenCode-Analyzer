
# GreenCode Analyzer
# Sustainable Industrial Improvement Simulation


def simulate_improvement(
    baseline_energy,
    baseline_emissions,
    energy_reduction_percent,
    emission_reduction_percent
):
    """
    Simulate potential energy and carbon reduction
    after sustainable improvements.
    """

    if baseline_energy < 0 or baseline_emissions < 0:
        raise ValueError("Baseline values cannot be negative.")

    if not 0 <= energy_reduction_percent <= 100:
        raise ValueError("Energy reduction must be between 0 and 100.")

    if not 0 <= emission_reduction_percent <= 100:
        raise ValueError("Emission reduction must be between 0 and 100.")

    # Calculate energy savings
    energy_saved = (
        baseline_energy * energy_reduction_percent / 100
    )

    # Calculate remaining energy
    optimized_energy = baseline_energy - energy_saved

    # Calculate emission reduction
    emissions_saved = (
        baseline_emissions * emission_reduction_percent / 100
    )

    # Calculate remaining emissions
    optimized_emissions = baseline_emissions - emissions_saved

    return {
        "baseline_energy": baseline_energy,
        "optimized_energy": optimized_energy,
        "energy_saved": energy_saved,
        "baseline_emissions": baseline_emissions,
        "optimized_emissions": optimized_emissions,
        "emissions_saved": emissions_saved,
        "energy_reduction_percent": energy_reduction_percent,
        "emission_reduction_percent": emission_reduction_percent
    }
if __name__ == "__main__":

    results = simulate_improvement(
        baseline_energy=1000,
        baseline_emissions=500,
        energy_reduction_percent=5,
        emission_reduction_percent=10
    )

    print("\n===== SUSTAINABLE IMPROVEMENT REPORT =====")

    for key, value in results.items():
        print(f"{key}: {value:,.2f}")