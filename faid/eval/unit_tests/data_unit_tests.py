from faid.logging import DataCard, get_data_entry, warning_msg, error_msg, success_msg

def get_fairness_entities_from_data():
    d = DataCard()
    return {
        "summary": get_data_entry('description').get('summary', ""),
        "data_subjects": get_data_entry('content').get('data_subjects', []),
        "protected_characteristics": get_data_entry('sensitive_data').get('protected_characteristics', []),
        "intentional_sensitive_data": get_data_entry('senstive_data').get('intentional_sensitive_data', []),
        "unintentional_sensitive_data": get_data_entry('senstive_data').get('unintentional_sensitive_data', []),
        "collection_protocol": get_data_entry("collection_protocol") or d.collection_protocol_schema,
    }

def test_fairness_stats_of_data():
    stats = get_data_entry("descriptive_statistics").get("stats", None)
    if stats is None:
        warning_msg("No stats found")
    else:
        for stat in stats:
            name = stat.get("name")
            value = stat.get("value")
            threshold = stat.get("threshold")
            bigger_is_better = stat.get("bigger_is_better")
            if bigger_is_better:
                if value >= threshold:
                    success_msg(f"TEST: {name}: PASS")
                else:
                    error_msg(f"TEST: {name} FAIL")
            else:
                if value <= threshold:
                    success_msg(f"TEST: {name}: PASS")
                else:
                    error_msg(f"TEST: {name} FAIL")


def test_sensitive_characteristics_featuring_in_data():
    data = get_data_entry('sensitive_data').get('protected_characteristics', [])
    if len(data) == 0:
        warning_msg("The data does not contain any protected characteristic data. Please check any proxy variables that can correlate with protected characteristics.")
    else:
        warning_msg("The data contains protected characteristic data. Please check if the data is being used in a way that is unaware of these characteristics.")



