from os.path import join, exists
import re
from collections import defaultdict
from shutil import copy

from faid.logging import error_msg, warning_msg, success_msg, update, load, get_project_log_path, get_current_folder_path

model_file_path = join(get_project_log_path(), "model.yml")
model_file_template_path = join(get_current_folder_path(), "templates/model.yml")
model_info_key = "model_info"

def initialize_model_log():
    if not exists(model_file_path):
        copy(model_file_template_path, model_file_path)
        success_msg("Model log file created.")
    else:
        warning_msg("Model log file already exists.  Logging will be appended to the existing file.")

def get_model_log_file_path():
    return model_file_path

def add_model_entry(params:dict, key:str="model_info"):
    update(params, key=key, filename=model_file_path)
    print(f"Added {key} to model card")

def get_model_entry(key:str=None):
    if key is None:
        return load(model_file_path)
    else:
        try:
            return load(model_file_path)[key]
        except KeyError:
            error_msg(f"Key {key} not found in the metadata file")
            return None

lookup_table = {
    "schema_version": "Not directly mapped; can be inferred from the Hugging Face spec.",
    "model_details": {
        "name": "{{ model_id | default('Model ID', true) }}",
        "overview": "{{ model_summary | default('', true) }}",
        "documentation": "{{ model_description | default('', true) }}",
        "owners": "{{ developers | default('[More Information Needed]', true) }}",
        "version": "{{ model_type | default('[More Information Needed]', true) }}",
        "licenses": "{{ license | default('[More Information Needed]', true) }}",
        "references": "{{ repo | default('[More Information Needed]', true) }}",
        "citations": {
            "APA": "{{ citation_apa | default('[More Information Needed]', true) }}",
            "BibTeX": "{{ citation_bibtex | default('[More Information Needed]', true) }}"
        },
        "path": "Not explicitly covered in the Hugging Face template."
    },
    "model_parameters": {
        "model_architecture": "{{ model_specs | default('[More Information Needed]', true) }}",
        "data": "{{ training_data | default('[More Information Needed]', true) }}",
        "input_format": "Not explicitly covered in Hugging Face.",
        "input_format_map": "Not explicitly covered in Hugging Face.",
        "output_format": "Not explicitly covered in Hugging Face.",
        "output_format_map": "Not explicitly covered in Hugging Face."
    },
    "quantitative_analysis": {
        "performance_metrics": "{{ testing_metrics | default('[More Information Needed]', true) }}",
        "graphics": "{{ results_summary | default('', true) }}"
    },
    "considerations": {
        "users": "{{ direct_use | default('[More Information Needed]', true) }}",
        "use_cases": "{{ downstream_use | default('[More Information Needed]', true) }}",
        "limitations": "{{ bias_risks_limitations | default('[More Information Needed]', true) }}",
        "tradeoffs": "{{ bias_risks_limitations | default('[More Information Needed]', true) }}",
        "ethical_considerations": "{{ bias_risks_limitations | default('[More Information Needed]', true) }}"
    },
    "definitions": {
        "owner": "{{ developers | default('[More Information Needed]', true) }}",
        "version": "{{ model_type | default('[More Information Needed]', true) }}",
        "license": "{{ license | default('[More Information Needed]', true) }}",
        "reference": "{{ repo | default('[More Information Needed]', true) }}",
        "citation": {
            "APA": "{{ citation_apa | default('[More Information Needed]', true) }}",
            "BibTeX": "{{ citation_bibtex | default('[More Information Needed]', true) }}"
        },
        "keyval": "Not explicitly covered in Hugging Face.",
        "dataset": "{{ training_data | default('[More Information Needed]', true) }}",
        "performance_metric": "{{ testing_metrics | default('[More Information Needed]', true) }}",
        "sensitive_data": "{{ bias_risks_limitations | default('[More Information Needed]', true) }}",
        "graphics_collection": "{{ results_summary | default('', true) }}",
        "graphic": "{{ results_summary | default('', true) }}",
        "user": "{{ direct_use | default('[More Information Needed]', true) }}",
        "use_case": "{{ downstream_use | default('[More Information Needed]', true) }}",
        "limitation": "{{ bias_risks_limitations | default('[More Information Needed]', true) }}",
        "tradeoff": "{{ bias_risks_limitations | default('[More Information Needed]', true) }}",
        "risk": "{{ bias_risks_limitations | default('[More Information Needed]', true) }}"
    }
}

def parse_markdown_to_dict(markdown_content):
    """
    Parse Huggingface's Markdown content into a dictionary.
    :param markdown_content: str, the content of the markdown file.
    :return: dict, parsed data from the markdown.
    """
    result = defaultdict(str)
    
    # Regular expressions to capture headers and their content
    header_pattern = re.compile(r"^(#+)\s+(.*)")
    key_value_pattern = re.compile(r"^\*\*([^:]+):\*\*\s*(.*)")

    stack = []  # To keep track of the current hierarchy
    current_dict = result

    lines = markdown_content.splitlines()
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue

        header_match = header_pattern.match(line)
        key_value_match = key_value_pattern.match(line)

        if header_match:
            level = len(header_match.group(1))
            header = header_match.group(2).strip()
            
            # Adjust stack to the current header level
            while len(stack) >= level:
                stack.pop()
            
            stack.append(header)

            # Traverse the dictionary to the correct level
            current_dict = result
            for key in stack[:-1]:
                current_dict = current_dict[key]
            
            # Create a new sub-dictionary
            if header not in current_dict:
                current_dict[header] = {}
            current_dict = current_dict[header]
        
        elif key_value_match:
            key = key_value_match.group(1).strip()
            value = key_value_match.group(2).strip()
            current_dict[key] = value

    return result

# Function to map from schema1 to schema2
def convert_to_hf_model_card(data, lookup_table):
    converted_data = {}
    for key, value in data.items():
        if key in lookup_table:
            converted_data[lookup_table[key]] = value
        else:
            warning_msg(f"Warning: No mapping found for key '{key}'")
    return converted_data

# Function to map from schema2 to schema1
def convert_to_google_model_card(data, lookup_table):
    # Reverse the lookup table for schema2 to schema1 conversion
    reversed_lookup = {v: k for k, v in lookup_table.items()}
    converted_data = {}
    for key, value in data.items():
        if key in reversed_lookup:
            converted_data[reversed_lookup[key]] = value
        else:
            warning_msg(f"Warning: No mapping found for key '{key}'")
    return converted_data

# Example JSON data in schema1
schema1_data = {
    "schema1_field1": "value1",
    "schema1_field2": "value2",
    "schema1_field3": "value3",
}

# Convert schema1 to schema2
#schema2_data = convert_to_hf_model_card(schema1_data, lookup_table)
#print("Schema2 Data:", dumps(schema2_data, indent=2))

# Convert schema2 back to schema1
#reverted_schema1_data = convert_to_google_model_card(schema2_data, lookup_table)
#print("Reverted Schema1 Data:", dumps(reverted_schema1_data, indent=2))


class ModelCard:        
        def __init__(self):
            # if model log file exists, load the metadata
            self.details_schema = {
                "name": "",
                "overview": "",
                "documentation": "",
                "owners": [
                    {
                        "name": "",
                        "contact": ""
                    }
                ],
                "version": {
                    "name": "",
                    "date": "",
                    "diff": ""
                },
                "license": {
                    "identifier": "",
                    "custom_text": ""
                },
                "references": "",
                "citation": "",
                "path": ""
            }
            self.model_params_schema = {
                "description": "",
                "model_architecture": "",
                "data": [
                    {
                        "description": "",
                        "link": "",
                        "sensitive": "",
                        "graphics": ""
                    }
                ],
                "input_format": "",
                "output_format": "",
                "output_format_map": ""
            }
            self.performance_metric_schema = {
                "name": "",
                "description": "",
                "value": "",
                "slice": "",
                "confidence_interval": {
                    "description": "",
                    "lower_bound": "",
                    "upper_bound": ""
                }
            }
            self.quantitive_analysis_schema = {
                "description": "",
                "performance_metrics": [self.performance_metric_schema]
            }
            self.risk_schema = {
                "name": "",
                "mitigation_strategy": ""
            }
            self.consideration_schema = {
                "description": "",
                "intended_users": "",
                "use_cases": "",
                "limitations": "",
                "tradeoffs": "",
                "ethical_considerations": "",
                "risks": [
                    self.risk_schema
                ]
            }

            self.model_info = load(model_file_path)["model_info"]
            #print("Model info is loaded from the model log file.")

        def get_model_info(self):
            """
            Returns the entire model information.
            """
            return self.model_info

        def set_model_info(self, model_info:dict):
            """
            Sets the model information with new info.
            """
            self.model_info = model_info

        def get_model_details(self):
            """
            Returns a specific detail from the model details.
            """
            return self.model_info.get("model_details", self.details_schema)

        def set_model_details(self, details, detail_key:str=None):
            """
            Sets a specific detail in the model details.
            """
            details = self.model_info.get("model_details", self.details_schema)
            if detail_key is None:
                self.model_info["model_details"] = details
            else:
                self.model_info["model_details"][detail_key] = details

        def get_model_parameters(self):
            """
            Returns a specific parameter from the model parameters.
            """
            return self.model_info.get("model_parameters", self.model_params_schema)

        def set_model_parameters(self, parameter_value, parameter_key:str=None):
            """
            Sets a specific parameter in the model parameters.
            """
            model_params = self.model_info.get("model_parameters", self.model_params_schema)
            if parameter_key is None:
                self.model_info["model_parameters"] = model_params
            else:
                self.model_info["model_parameters"][parameter_key] = parameter_value

        def get_quantitative_analysis(self):
            """
            Returns a specific metric from the quantitative analysis.
            """
            return self.model_info.get("quantitative_analysis", self.quantitive_analysis_schema)

        def get_performance_metric(self, metric_name):
            """
            Returns a specific metric from the quantitative analysis.
            """
            metrics = self.model_info.get("quantitative_analysis", self.quantitive_analysis_schema).get("performance_metrics", [self.performance_metric_schema])
            for metric in metrics:
                if metric.get("name") == metric_name:
                    return metric
                else:
                    error_msg(f"Metric {metric_name} not found in the model log file.")
                    return None

        def add_quantitative_analysis_metric(self, metric:dict):
            """
            Adds a new metric to the quantitative analysis.
            If a metric with the same name already exists, it will be updated with the new value.
            """
            quantitative_analysis = self.model_info.get("quantitative_analysis", self.quantitive_analysis_schema)
            metrics = quantitative_analysis.get("performance_metrics", [])
            
            metric_name = metric.get("name")
            if not metric_name:
                error_msg("Metric must have a name.")
                return
            
            for i, existing_metric in enumerate(metrics):
                if existing_metric.get("name") == metric_name:
                    metrics[i] = {**existing_metric, **metric}
                    warning_msg(f"Metric {metric_name} already exists. It has been updated with the new value.")
                    break
            else:
                metrics.append(metric)
            
            self.model_info["quantitative_analysis"]["performance_metrics"] = metrics

        def get_considerations(self):
            """
            Returns a specific consideration from the considerations section.
            """
            return self.model_info.get("considerations", self.consideration_schema)

        def add_consideration(self, consideration_key, consideration):
            """
            Adds a new consideration to the considerations section.
            """
            
            if "considerations" not in self.model_info:
                self.model_info["considerations"] = self.consideration_schema
            # if consideration_key is "risks", it should comply with schema
            if consideration_key == "risks":
                risks = self.model_info["considerations"].get("risks", self.risk_schema)
                consideration = {**self.risk_schema, **consideration}
                risks.append(consideration)
                self.model_info["considerations"]["risks"] = risks
            else:
                self.model_info["considerations"][consideration_key] = consideration

        def save(self):
            """
            Saves the model information to the model log file.
            """
            update(self.model_info, key=model_info_key, filename=model_file_path)
            success_msg("Model info saved to the model log file.")
        
        def to_dict(self):
            """
            Returns the model information as a dictionary.
            """
            return self.model_info