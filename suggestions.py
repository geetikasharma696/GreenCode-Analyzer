
def generate_suggestions(
    nested_loops,
    for_loops,
    while_loops,
    membership_checks
):

    suggestions = []

    if nested_loops:
        suggestions.append({
            "issue": "Nested Loop Detected",
            "severity": "Medium",
            "suggestion": (
                "Review whether nested iteration is necessary. "
                "Consider using dictionaries or sets where appropriate."
            )
        })

    # Analyze membership checks by collection type
    list_checks = [
        check for check in membership_checks
        if check["type"] == "list"
    ]

    set_checks = [
        check for check in membership_checks
        if check["type"] == "set"
    ]

    dictionary_checks = [
        check for check in membership_checks
        if check["type"] == "dictionary"
    ]

    unknown_checks = [
        check for check in membership_checks
        if check["type"] == "unknown"
    ]

    if list_checks:
        suggestions.append({
            "issue": "List Membership Check Inside Loop",
            "severity": "Medium",
            "suggestion": (
                "Repeated membership checks in a list can take "
                "O(n) average time per lookup. If appropriate, "
                "consider converting the list to a set for "
                "average O(1) lookup."
            )
        })

    if set_checks:
        suggestions.append({
            "issue": "Set Membership Check",
            "severity": "Info",
            "suggestion": (
                "A set already provides average O(1) membership "
                "lookup. No list-to-set optimization is needed."
            )
        })

    if dictionary_checks:
        suggestions.append({
            "issue": "Dictionary Membership Check",
            "severity": "Info",
            "suggestion": (
                "Dictionary key membership generally provides "
                "average O(1) lookup. Ensure the intended check "
                "is against dictionary keys."
            )
        })

    if unknown_checks:
        suggestions.append({
            "issue": "Unknown Collection Type",
            "severity": "Info",
            "suggestion": (
                "The collection type could not be identified. "
                "Review the membership check manually."
            )
        })

    if for_loops > 5:
        suggestions.append({
            "issue": "High Number of For Loops",
            "severity": "Low",
            "suggestion": (
                "Review repeated iterations and check whether "
                "some operations can be combined or avoided."
            )
        })

    if while_loops > 5:
        suggestions.append({
            "issue": "High Number of While Loops",
            "severity": "Low",
            "suggestion": (
                "Review loop conditions and unnecessary repeated "
                "processing."
            )
        })

    if not suggestions:
        suggestions.append({
            "issue": "No Known Pattern Detected",
            "severity": "Info",
            "suggestion": (
                "No configured optimization rule was triggered. "
                "This does not guarantee that the code is efficient."
            )
        })

    return suggestions
