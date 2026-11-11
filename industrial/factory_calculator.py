
GJ_TO_KWH = 277.7777778


def calculate_factory_energy(
    annual_production,
    energy_intensity,
    improvement_percent=5
):
    """
    Calculate baseline energy consumption
    and potential energy savings for a steel factory.
    """

    if annual_production <= 0:
        raise ValueError("Annual production must be greater than zero.")

    if energy_intensity <= 0:
        raise ValueError("Energy intensity must be greater than zero.")

    if not 0 <= improvement_percent <= 100:
        raise ValueError("Improvement must be between 0 and 100.")

    # 1. Calculate annual energy in GJ
    annual_energy_gj = annual_production * energy_intensity

    # 2. Convert GJ into kWh-equivalent
    annual_energy_kwh = annual_energy_gj * GJ_TO_KWH

    # 3. Calculate daily average energy
    daily_energy_kwh = annual_energy_kwh / 365

    # 4. Calculate energy savings
    energy_saved_kwh = (
        annual_energy_kwh * improvement_percent / 100
    )

    energy_saved_gj = (
        annual_energy_gj * improvement_percent / 100
    )

    # 5. Calculate remaining energy after improvement
    remaining_energy_kwh = annual_energy_kwh - energy_saved_kwh

    return {
        "annual_production": annual_production,
        "energy_intensity": energy_intensity,
        "annual_energy_gj": annual_energy_gj,
        "annual_energy_kwh_equivalent": annual_energy_kwh,
        "daily_energy_kwh_equivalent": daily_energy_kwh,
        "improvement_percent": improvement_percent,
        "energy_saved_gj": energy_saved_gj,
        "energy_saved_kwh_equivalent": energy_saved_kwh,
        "remaining_energy_kwh_equivalent": remaining_energy_kwh
    }


if __name__ == "__main__":

    results = calculate_factory_energy(
        annual_production=500000,
        energy_intensity=20.95,
        improvement_percent=5
    )

    print("\n===== STEEL FACTORY ENERGY REPORT =====")

    for key, value in results.items():
        print(f"{key}: {value:,.2f}")
