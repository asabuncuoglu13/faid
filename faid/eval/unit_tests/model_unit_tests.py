from faid.logging import ModelCard, get_model_entry

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