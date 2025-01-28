from faid.logging import (
    error_msg, 
    warning_msg,
    success_msg,
    load,
    get_fairness_entities_from_data,
    get_fairness_entities_from_model,
    ModelCard,
)

def test_model_metadata_values():
    m = ModelCard()
    fdata_schema = {
        "model_parameters" : m.model_params_schema,
        "quantitative_analysis": m.quantitive_analysis_schema,
        "considerations": m.consideration_schema,
    }
    fdata = get_fairness_entities_from_model()
    fdata = {**fdata_schema, **fdata}

    for key, value in fdata.items():
        if value is None: 
            warning_msg(f"Value for key {key} is None")
        else:
            print(f"{key}: {value}")
    
    for metric in fdata.get("quantitative_analysis").get("performance_metrics"):
        print(f"Checking metric: {metric.get('name')}. The metric description: {metric.get('description')}")
        try:
            metric_value = float(metric.get("value"))
            lower_bound = float(metric.get("confidence_interval").get("lower_bound"))
            upper_bound = float(metric.get("confidence_interval").get("upper_bound"))
            
            if metric_value < lower_bound:
                error_msg(f"Value for {metric.get('name')} is lower than the lower bound of the confidence interval")
            elif metric_value > upper_bound:
                error_msg(f"Value for {metric.get('name')} is higher than the upper bound of the confidence interval")
            else:
                success_msg(f"Value for {metric.get('name')} is within the confidence interval")
        except (ValueError, TypeError):
            warning_msg(f"Value or confidence interval bounds for {metric.get('name')} are not convertible to floats.")


