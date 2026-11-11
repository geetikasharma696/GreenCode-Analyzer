
def calculate_carbon_emissions(
    electricity_kwh,
    electricity_emission_factor,
    fuel_energy_gj,
    fuel_emission_factor
):
    """
    Calculate CO2 emissions from electricity and fuel.

    Electricity emission factor: kg CO2 per kWh
    Fuel emission factor: kg CO2 per GJ
    """

    if electricity_kwh < 0 or fuel_energy_gj < 0:
        raise ValueError("Energy consumption cannot be negative.")

    if electricity_emission_factor < 0 or fuel_emission_factor < 0:
        raise ValueError("Emission factors cannot be negative.")

    # Electricity-related emissions
    electricity_emissions = (
        electricity_kwh * electricity_emission_factor
    )

    # Fuel-related emissions
    fuel_emissions = fuel_energy_gj * fuel_emission_factor

    # Total emissions
    total_emissions = electricity_emissions + fuel_emissions

    return {
        "electricity_emissions_kg": electricity_emissions,
        "fuel_emissions_kg": fuel_emissions,
        "total_emissions_kg": total_emissions,
        "total_emissions_tonnes": total_emissions / 1000
    }
if __name__ == "__main__":

    results = calculate_carbon_emissions(
        electricity_kwh=1000,
        electricity_emission_factor=0.7,
        fuel_energy_gj=100,
        fuel_emission_factor=56.1
    )

    print("\n===== INDUSTRIAL CARBON REPORT =====")

    for key, value in results.items():
        print(f"{key}: {value:,.2f}")