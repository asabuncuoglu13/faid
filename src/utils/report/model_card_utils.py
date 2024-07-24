# %%
class ModelCardUtils:
    def __init__(self, model_info=None):
        if model_info is None:
            model_info = {}
        self.model_info = model_info

    def get_model_info(self):
        """
        Returns the entire model information.
        """
        return self.model_info

    def set_model_info(self, new_info):
        """
        Sets the model information with new info.
        """
        self.model_info = new_info

    def get_model_detail(self, detail_key):
        """
        Returns a specific detail from the model details.
        """
        return self.model_info.get("model_details", {}).get(detail_key, None)

    def set_model_detail(self, detail_key, detail_value):
        """
        Sets a specific detail in the model details.
        """
        if "model_details" not in self.model_info:
            self.model_info["model_details"] = {}
        self.model_info["model_details"][detail_key] = detail_value

    def get_model_parameter(self, parameter_key):
        """
        Returns a specific parameter from the model parameters.
        """
        return self.model_info.get("model_parameters", {}).get(parameter_key, None)

    def set_model_parameter(self, parameter_key, parameter_value):
        """
        Sets a specific parameter in the model parameters.
        """
        if "model_parameters" not in self.model_info:
            self.model_info["model_parameters"] = {}
        self.model_info["model_parameters"][parameter_key] = parameter_value

    def get_quantitative_analysis(self, metric_key):
        """
        Returns a specific metric from the quantitative analysis.
        """
        metrics = self.model_info.get("quantitative_analysis", {}).get("performance_metrics", [])
        for metric in metrics:
            if metric.get("type") == metric_key:
                return metric
        return None

    def add_quantitative_metric(self, metric):
        """
        Adds a new metric to the quantitative analysis.
        """
        if "quantitative_analysis" not in self.model_info:
            self.model_info["quantitative_analysis"] = {"performance_metrics": []}
        self.model_info["quantitative_analysis"]["performance_metrics"].append(metric)

    def get_consideration(self, consideration_key):
        """
        Returns a specific consideration from the considerations section.
        """
        considerations = self.model_info.get("considerations", {}).get(consideration_key, [])
        return considerations

    def add_consideration(self, consideration_key, consideration):
        """
        Adds a new consideration to the considerations section.
        """
        if "considerations" not in self.model_info:
            self.model_info["considerations"] = {}
        if consideration_key not in self.model_info["considerations"]:
            self.model_info["considerations"][consideration_key] = []
        self.model_info["considerations"][consideration_key].append(consideration)


# %% Create test cases
model_info = ModelCardUtils()
model_info.set_model_detail("model_name", "BERT")
model_info.set_model_parameter("num_layers", 12)
model_info.add_quantitative_metric({"type": "accuracy", "value": 0.95})
model_info.add_consideration("ethical_considerations", "This model is not fair.")