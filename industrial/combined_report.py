
# GreenCode Analyzer
# Combined Industrial Sustainability Report


def generate_combined_report(
    factory_results,
    process_results,
    recommendations,
    energy_simulation,
    carbon_results
):

    report = []

    report.append("=" * 55)
    report.append(" INDUSTRIAL SUSTAINABILITY REPORT")
    report.append(" GREEN CODE ANALYZER")
    report.append("=" * 55)

    # 1. Factory Energy Analysis
    report.append("\n1. FACTORY ENERGY ANALYSIS")

    report.append(
        f"Annual Production: "
        f"{factory_results['annual_production']:,.0f} tonnes"
    )

    report.append(
        f"Energy Intensity: "
        f"{factory_results['energy_intensity']} GJ/tonne"
    )

    report.append(
        f"Annual Energy: "
        f"{factory_results['annual_energy_gj']:,.2f} GJ"
    )

    # 2. Process-wise Energy Analysis
    report.append("\n2. PROCESS-WISE ENERGY ANALYSIS")

    report.append(
        f"Total Process Energy: "
        f"{process_results['total_energy_gj']:,.2f} GJ"
    )

    report.append(
        f"Highest Energy Consumer: "
        f"{process_results['highest_energy_process']}"
    )

    for process, details in process_results["process_results"].items():

        report.append(
            f"{process}: {details['energy_gj']:,.2f} GJ "
            f"({details['share_percent']:.2f}%)"
        )

    # 3. Sustainability Recommendations
    report.append("\n3. SUSTAINABILITY RECOMMENDATIONS")

    for item in recommendations:

        report.append(
            f"{item['process']}: {item['recommendation']}"
        )

    # 4. Energy Improvement Simulation
    report.append("\n4. BEFORE VS AFTER ENERGY ANALYSIS")

    report.append(
        f"Before Improvement: "
        f"{energy_simulation['total_before_gj']:,.2f} GJ"
    )

    report.append(
        f"After Improvement: "
        f"{energy_simulation['total_after_gj']:,.2f} GJ"
    )

    report.append(
        f"Energy Saved: "
        f"{energy_simulation['total_saved_gj']:,.2f} GJ"
    )

    report.append(
        f"Energy Reduction: "
        f"{energy_simulation['overall_reduction_percent']:.2f}%"
    )

    # 5. Carbon Reduction Analysis
    report.append("\n5. BEFORE VS AFTER CARBON ANALYSIS")

    report.append(
        f"Before Improvement: "
        f"{carbon_results['total_before_kg']:,.2f} kg CO2"
    )

    report.append(
        f"After Improvement: "
        f"{carbon_results['total_after_kg']:,.2f} kg CO2"
    )

    report.append(
        f"CO2 Saved: "
        f"{carbon_results['total_saved_kg']:,.2f} kg"
    )

    report.append(
        f"CO2 Reduction: "
        f"{carbon_results['reduction_percent']:.2f}%"
    )

    # 6. Important Note
    report.append("\n6. REPORT NOTES")

    report.append(
        "Energy and carbon improvement figures are simulations."
    )

    report.append(
        "Illustrative inputs must not be treated as actual factory measurements."
    )

    report.append(
        "Use verified factory data and emission factors for real assessments."
    )

    report.append("\n" + "=" * 55)
    report.append(" END OF INDUSTRIAL SUSTAINABILITY REPORT")
    report.append("=" * 55)

    return "\n".join(report)
