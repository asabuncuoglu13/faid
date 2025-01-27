from os.path import join, exists
from json import dumps
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
        def __init__(self, model_info:dict={}):
            # if model log file exists, load the metadata
            if model_info:
                self.model_info = model_info
                print("Model info is created with the provided dictionary.")
            else:
                self.model_info = load(model_file_path)["model_info"]
                print("Model info is loaded from the model log file.")

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
            details_schema = {
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
            if "model_details" not in self.model_info:
                self.model_info["model_details"] = details_schema
            details_schema[detail_key] = detail_value
            self.model_info["model_details"] = details_schema

        def get_model_parameter(self, parameter_key):
            """
            Returns a specific parameter from the model parameters.
            """
            return self.model_info.get("model_parameters", {}).get(parameter_key, None)

        def set_model_parameter(self, parameter_key, parameter_value):
            """
            Sets a specific parameter in the model parameters.
            """
            model_params = {}
            {
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
            model_params[parameter_key] = parameter_value
            self.model_info["model_parameters"] = model_params

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
            
            metric_schema = {
                "description": "",
                "value": "",
                "slice": "",
                "confidence_interval": {
                    "description": "",
                    "lower_bound": "",
                    "upper_bound": ""
                }
            }
            metric = {**metric_schema, **metric}
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
            risk_schema = {
                "name": "",
                "mitigation_strategy": ""
            }
            consideration_schema = {
                "description": "",
                "intended_users": "",
                "use_cases": "",
                "limitations": "",
                "tradeoffs": "",
                "ethical_considerations": "",
                "risks": [
                    risk_schema
                ]
            }
            if "considerations" not in self.model_info:
                self.model_info["considerations"] = consideration_schema
            # if consideration_key is "risks", it should comply with schema
            if consideration_key == "risks":
                risks = self.model_info["considerations"].get("risks", [])
                consideration = {**risk_schema, **consideration}
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