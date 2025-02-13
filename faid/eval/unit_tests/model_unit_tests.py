from faid.logging import ModelCard, get_model_entry, warning_msg, error_msg, success_msg

def get_fairness_entities_from_model():
    m = ModelCard()
    model_info = get_model_entry("model_info")
    return {
        "model_parameters" : {
            "data": model_info.get("model_parameters", m.model_params_schema).get('data', None),
        },
        "quantitative_analysis": model_info.get("quantitative_analysis", m.quantitive_analysis_schema),
        "considerations": model_info.get("considerations", m.consideration_schema)
    }

def test_fairness_stats_of_model():
    stats = get_model_entry("quantitative_analysis").get("performance_metrics", None)
    if stats is None:
        warning_msg("No metric stats found")
    else:
        for stat in stats:
            name = stat.get("name")
            value = stat.get("value")
            interval = stat.get("confidence_interval")
            print(f"The success interval is defined based on: {interval["description"]}")
            if value >= interval["lower_bound"] and value <= interval["upper_bound"]:
                success_msg(f"TEST: {name}: PASS")
            else:
                error_msg(f"TEST: {name} FAIL")

def test_fairness_by_unawareness():
    data = get_model_entry('model_parameters').get('data', [])
    if len(data) == 0:
        warning_msg("The model metadata does not contain any data-related information. Please check if the model is being used in a way that is unaware of the sensitive data.")
    else:
        for d in data:
            if d.get('sensitive') is not None:
                warning_msg("The model metadata contains sensitive data. Please check if the model is being used in a way that is unaware of these characteristics.")
                break