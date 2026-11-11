
# GreenCode Analyzer
# Combined Industrial Sustainability Report

from industrial.factory_calculator import calculate_factory_energy
from industrial.carbon_calculator import calculate_carbon_emissions
from industrial.optimization import simulate_improvement


def generate_industrial_report():

    # 1. Factory energy calculation
    factory = calculate_factory_energy(
        annual_production=500000,
        energy_intensity=20.95,
        improvement_percent=5
    )

    # 2. Carbon emission calculation
    # Example values for testing only
    carbon = calculate_carbon_emissions(
        electricity_kwh=1000,
        electricity_emission_factor=0.7,
        fuel_energy_gj=100,
        fuel_emission_factor=56.1
    )

    # 3. Sustainable improvement simulation
    improvement = simulate_improvement(
        baseline_energy=factory["annual_energy_kwh_equivalent"],
        baseline_emissions=carbon["total_emissions_kg"],
        energy_reduction_percent=5,
        emission_reduction_percent=10
    )

    # 4. Display combined report
    print("\n======================================")
    print(" INDUSTRIAL SUSTAINABILITY REPORT")
    print("======================================")

    print("\n--- FACTORY ENERGY ANALYSIS ---")
    print(f"Annual Production: {factory['annual_production']:,.0f} tonnes")
    print(f"Energy Intensity: {factory['energy_intensity']} GJ/tonne")
    print(f"Annual Energy: {factory['annual_energy_gj']:,.2f} GJ")
    print(f"Annual Energy Equivalent: {factory['annual_energy_kwh_equivalent']:,.2f} kWh")
    print(f"Daily Energy Equivalent: {factory['daily_energy_kwh_equivalent']:,.2f} kWh")

    print("\n--- CARBON EMISSION ANALYSIS ---")
    print(f"Electricity Emissions: {carbon['electricity_emissions_kg']:,.2f} kg CO2")
    print(f"Fuel Emissions: {carbon['fuel_emissions_kg']:,.2f} kg CO2")
    print(f"Total Emissions: {carbon['total_emissions_kg']:,.2f} kg CO2")
    print(f"Total Emissions: {carbon['total_emissions_tonnes']:.2f} tonnes CO2")

    print("\n--- SUSTAINABLE IMPROVEMENT ---")
    print(f"Energy Saved: {improvement['energy_saved']:,.2f} kWh-equivalent")
    print(f"Optimized Energy: {improvement['optimized_energy']:,.2f} kWh-equivalent")
    print(f"Emissions Saved: {improvement['emissions_saved']:,.2f} kg CO2")
    print(f"Optimized Emissions: {improvement['optimized_emissions']:,.2f} kg CO2")

    print("\n======================================")


if __name__ == "__main__":
    generate_industrial_report()

