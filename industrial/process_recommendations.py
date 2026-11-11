
# GreenCode Analyzer
# Industrial Sustainability Recommendation Engine


def generate_process_recommendations(process_results):

    recommendations = []

    process_data = process_results["process_results"]

    for process, details in process_data.items():

        energy = details["energy_gj"]
        share = details["share_percent"]

        if process == "Furnace":

            recommendations.append({
                "process": process,
                "energy_share": share,
                "recommendation": (
                    "Inspect furnace insulation, reduce heat loss, "
                    "and recover waste heat wherever technically feasible."
                )
            })

        elif process == "Rolling Mill":

            recommendations.append({
                "process": process,
                "energy_share": share,
                "recommendation": (
                    "Optimize rolling schedules, maintain motors, "
                    "and reduce unnecessary machine idle time."
                )
            })

        elif process == "Motors and Pumps":

            recommendations.append({
                "process": process,
                "energy_share": share,
                "recommendation": (
                    "Use energy-efficient motors, maintain pumps, "
                    "and consider variable frequency drives."
                )
            })

        elif process == "Compressed Air":

            recommendations.append({
                "process": process,
                "energy_share": share,
                "recommendation": (
                    "Detect air leaks, maintain pressure levels, "
                    "and avoid unnecessary compressed air usage."
                )
            })

    recommendations.sort(
        key=lambda item: item["energy_share"],
        reverse=True
    )

    return recommendations
