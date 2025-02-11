from os.path import join, exists
from shutil import copy

from faid.logging import error_msg, warning_msg, success_msg, update, load, get_project_log_path, get_current_folder_path

data_file_path = join(get_project_log_path(), "data.yml")
data_file_template_path = join(get_current_folder_path(), "templates/data.yml")

def initialize_data_log():
    if not exists(data_file_path):
        copy(data_file_template_path, data_file_path)
        success_msg("Data log file created.")
    else:
        warning_msg("Data log file already exists. Logging will be appended to the existing file.")

def get_data_log_path():
    return data_file_path

def add_data_entry(key:str, entry:any):
    """
    Add a data entry to the data card
    """
    if type(entry) is dict:
        try:
            if entry.get("conformsTo") == 'http://mlcommons.org/croissant/RAI/1.0':
                key="rai"
        except AttributeError | KeyError:
            pass
    update(entry, key=key, filename=data_file_path)
    print(f"Added {key} to data card")

def get_data_entry(key:str=None):
    if key is None:
        return load(data_file_path)
    else:
        try:
            return load(data_file_path)[key]
        except AttributeError | KeyError:
            error_msg(f"Key {key} not found in the metadata file")
            return None

def pretty_croissant(ds) -> dict:
    """
    Gets the ML Croissant metadata dict and returns another dict with our report format
    """
    import itertools
    import pandas as pd
    metadata = ds.metadata.to_json()
    records = ds.records("conversations")

    df = pd.DataFrame(list(itertools.islice(records, 10)))
    return {
        "description": {
            "name": metadata.get("name", ""),
            "summary": metadata.get("description", ""),
            "dataset_link": metadata.get("url", ""),
            "authors": metadata.get("citeAs", ""),
            "publishing_organization": metadata.get("publisher", ""),
            "owners": metadata.get("creator", []),
            "funding_sources": metadata.get("funding_sources", []),
            "publishing_poc":  metadata.get("publishing_poc", {}),
        },
        "content": {
            "description": metadata.get("content_description", ""),
            "data_subjects": metadata.get("data_subjects", []),
            "sampling_data_points": [df.head().to_dict()],
            "data_fields": df.keys().tolist(),
            "Total Records": metadata.get("dataset_snapshot", {}).get("Total Records", ""),
            "Coverage": metadata.get("dataset_snapshot", {}).get("Coverage", ""),
            "Time Span": metadata.get("dataset_snapshot", {}).get("Time Span", "")
        }
    }

def pretty_croissant_rai(metadata) -> dict:
    """
    Gets the ML Croissant metadata dict and returns another dict with our report format
    """
    return {
        "collection_protocol": {
            "data_collection": metadata.get("dataCollection", ""),
            "data_collection_type": metadata.get("dataCollectionType", ""),
            "data_collection_raw_data": metadata.get("dataCollectionRawData", ""),
            "data_annotation_protocol": metadata.get("dataAnnotationProtocol", ""),
            "data_annotation_platform": metadata.get("dataAnnotationPlatform", ""),
            "data_annotation_analysis": metadata.get("dataAnnotationAnalysis", ""),
            "data_use_cases": metadata.get("dataUseCases", ""),
            "annotations_per_item": metadata.get("annotationsPerItem", ""),
            "annotator_demographics": metadata.get("annotatorDemographics", "")
        }
    }

def pretty_uci_metadata(metadata) -> dict:
    """
    Gets the UCI metadata dict and returns another dict with our report format
    """
    return {
        "id": metadata.get("uci_id", ""),
        "description": {
            "dataset_name": metadata.get("name", ""),
            "dataset_link": metadata.get("data_url", ""),            
            "repository_url": metadata.get("repository_url", ""),
            "intro_paper": metadata.get("intro_paper", ""),
            "authors": metadata.get("creators", []),
            "summary": metadata.get("abstract", ""),
            "industry_types": metadata.get("area", ""),
            "tasks": metadata.get("tasks", []),
            "characteristics": metadata.get("characteristics", []),
            "feature_types": metadata.get("feature_types", []),
            "target_col": metadata.get("target_col", ""),
            "index_col": metadata.get("index_col", ""),
            "funding_sources": metadata.get("additional_info", "").get("funded_by", ""),
        },
        "content": {
            "data_fields": metadata.get("additional_info", "").get("variable_info", [])
        },
        "descriptive_statistics": {
            "num_instances": metadata.get("num_instances", ""),
            "num_features": metadata.get("num_features", ""),
            "has_missing_values": metadata.get("has_missing_values", False),
            "missing_values_symbol": metadata.get("missing_values_symbol", "")
        },
        "sensitive_data" : {
            "protected_characteristics": metadata.get("demographics", ""),
            "intentional_sensitive_data": metadata.get("additional_info", "").get("sensitive_data", ""),
        },
        "version_details": {
            "current_version": "",
            "last_updated": metadata.get("last_updated", ""),
            "release_date": metadata.get("year_of_dataset_creation", "")
        }
    }


class DataCard:
    def __init__(self):
        self.data_info = load(data_file_path)
        self.description_schema = {
            "name": "",
            "summary": "",
            "dataset_link": "",
            "repository_link": "",
            "intro_paper": "",
            "publishing_organization": "",
            "tasks": [],
            "characteristics": [],
            "feature_types": [],
            "target_col": "",
            "index_col": "",
            "year_of_dataset_creation": "",
            "last_updated": "",
            "industry_types": [],
            "publishing_poc": {},
            "owners": [],
            "authors": []
        }
        self.content_schema = {
            "description": "",
            "primary_data_modality": "",
            "has_missing_values": "",
            "missing_values_symbol": "",
            "sampling_data_points": [],
            "data_fields": [],
            "typical_data_point": "",
            "data_subjects": [],
            "dataset_snapshot": {
                "Total Records": "",
                "Coverage": "",
                "Time Span": ""
            }
        }
        self.descriptive_statistics_schema = {
            "num_instances": "",
            "num_features": "",
            "has_missing_values": "",
            "missing_values_symbol": "",
            "fields": [],
            "stats": [{
                "name": "",
                "description": "",
                "value": 0,
                "threshold": 0,
                "bigger_is_better": "",
                "label": "",
                "notes": "",
                "sg_params": {}
            }]
        }
        self.sensitive_data_schema = {
            "protected_characteristics": [],
            "intentional_sensitive_data": [],
            "unintentional_sensitive_data": [{
                "name": "",
                "description": ""
            }],
            "security_privacy_handling": ""
        }
        self.risks_schema = [{
            "name": "",
            "mitigation_strategy": ""
        }]
        self.version_details_schema = {
            "current_version": "",
            "last_updated": "",
            "release_date": "",
            "maintenance_status": "",
            "maintenance_plan": "",
            "next_update": {
            "version_affected": "",
            "next_data_update": "",
            "next_version": "",
            "next_version_update": ""
            },
            "expected_changes": ""
        }
        self.collection_protocol_schema = {
            "data_collection": "",
            "data_collection_type": "",
            "data_collection_raw_data": "",
            "data_annotation_protocol": "",
            "data_annotation_platform": "",
            "data_annotation_analysis": "",
            "annotations_per_item": "",
            "annotator_demographics": "",
            "data_use_cases": ""
        }

    def get_description(self):
        """
        Returns the description section from the data information.
        """
        return self.data_info.get("description", self.description_schema)

    def set_description(self, description: dict):
        """
        Sets the description section in the data information.
        """
        self.data_info["description"] = description

    def get_content(self):
        """
        Returns the content section from the data information.
        """
        return self.data_info.get("content", self.content_schema)

    def set_content(self, content: dict):
        """
        Sets the content section in the data information.
        """
        self.data_info["content"] = content

    def get_descriptive_statistics(self):
        """
        Returns the descriptive statistics section from the data information.
        """
        return self.data_info.get("descriptive_statistics", self.descriptive_statistics_schema)

    def add_new_stat(self, stat: dict):
        """
        Adds a new statistic to the descriptive statistics section.
        """
        descriptive_statistics = self.data_info.get("descriptive_statistics", self.descriptive_statistics_schema)
        descriptive_statistics["stats"].append(stat)
        self.data_info["descriptive_statistics"] = descriptive_statistics

    def set_descriptive_statistics(self, descriptive_statistics: dict):
        """
        Sets the descriptive statistics section in the data information.
        """
        self.data_info["descriptive_statistics"] = descriptive_statistics

    def get_sensitive_data(self):
        """
        Returns the sensitive data section from the data information.
        """
        return self.data_info.get("sensitive_data", self.sensitive_data_schema)

    def set_sensitive_data(self, sensitive_data: dict):
        """
        Sets the sensitive data section in the data information.
        """
        self.data_info["sensitive_data"] = sensitive_data

    def get_risks(self):
        """
        Returns the risks section from the data information.
        """
        return self.data_info.get("risks", self.risks_schema)

    def add_risk(self, risk: dict):
        """
        Adds a new risk to the risks section.
        """
        risks = self.data_info.get("risks", self.risks_schema)
        risks.append(risk)
        self.data_info["risks"] = risks

    def get_version_details(self):
        """
        Returns the version details section from the data information.
        """
        return self.data_info.get("version_details", self.version_details_schema)

    def set_version_details(self, version_details: dict):
        """
        Sets the version details section in the data information.
        """
        self.data_info["version_details"] = version_details

    def get_collection_protocol(self):
        """
        Returns the collection protocol section from the data information.
        """
        return self.data_info.get("collection_protocol", self.collection_protocol_schema)

    def set_collection_protocol(self, collection_protocol: dict):
        """
        Sets the collection protocol section in the data information.
        """
        self.data_info["collection_protocol"] = collection_protocol

    def save(self):
        """
        Saves the data information to the data log file.
        """
        update(self.data_info, filename=data_file_path)
        success_msg("Data info saved to the data log file.")

    def to_dict(self):
        """
        Returns the data information as a dictionary.
        """
        return self.data_info
