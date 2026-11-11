
def analyze_process_energy(process_data):

    if not process_data:
        raise ValueError("Please provide process energy data.")

    for process, energy in process_data.items():

        if energy < 0:
            raise ValueError(
                f"Energy consumption for {process} cannot be negative."
            )

    total_energy = sum(process_data.values())

    if total_energy <= 0:
        raise ValueError("Total energy consumption must be greater than zero.")

    process_results = {}

    for process, energy in process_data.items():

        share = (energy / total_energy) * 100

        process_results[process] = {
            "energy_gj": energy,
            "share_percent": share
        }

    highest_process = max(
        process_data,
        key=process_data.get
    )

    return {
        "total_energy_gj": total_energy,
        "process_results": process_results,
        "highest_energy_process": highest_process,
        "highest_energy_value_gj": process_data[highest_process]
    }
if __name__ == "__main__":

    sample_process_data = {
        "Furnace": 500,
        "Rolling Mill": 300,
        "Motors and Pumps": 150,
        "Compressed Air": 50
    }

    results = analyze_process_energy(sample_process_data)

    print("\n===== PROCESS-WISE ENERGY REPORT =====")

    print(f"\nTotal Energy: {results['total_energy_gj']} GJ")

    print("\nProcess-wise Details:")

    for process, details in results["process_results"].items():

        print(f"\nProcess: {process}")
        print(f"Energy: {details['energy_gj']} GJ")
        print(f"Energy Share: {details['share_percent']:.2f}%")

    print("\nHighest Energy Consuming Process:")
    print(results["highest_energy_process"])