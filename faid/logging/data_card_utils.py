from os.path import join, exists
from shutil import copy

from faid.logging import error_msg, update, load, get_project_log_path, get_current_folder_path

data_file_path = join(get_project_log_path(), "data.yml")
data_file_template_path = join(get_current_folder_path(), "templates/data.yml")
data_info_key = "dataset_info"

def initialize_data_log():
    if not exists(data_file_path):
        copy(data_file_template_path, data_file_template_path)
        print("Data log file created.")
    else:
        print("Data log file already exists.")

def get_data_log_path():
    return data_file_path

def add_data_entry(entry, key:str="dataset_info"):
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
        except KeyError:
            error_msg(f"Key {key} not found in the metadata file")
            return None

class DataCard:
    
    def __init__(self, dataset_info:dict=None, rai:dict=None):
        self.dataset_name = dataset_info
        self.rai = rai

    def to_dict(self):
        """
        Returns the data information as a dictionary.
        """
        return {
            "dataset_info": self.dataset_info,
            "rai": self.rai
        }

    def save(self):
        """
        Saves the data information to the data log file.
        """
        update(self.to_dict(), key=data_info_key, filename=data_file_path)
        print("Data info saved to the data log file.")

    def validate(self, schema):
        """
        Validates the data information against a schema.
        """
        from jsonschema import validate
        validate(instance=self.to_dict(), schema=schema)


def pretty_croissant(ds) -> dict:
    """
    Gets the ML Croissant metadata dict and returns another dict with our report format
    """
    import itertools
    import pandas as pd
    metadata = ds.metadata.to_json()
    records = ds.records("conversations")

    df = pd.DataFrame(list(itertools.islice(records, 10)))
    dataset_info = {
        "dataset_name": metadata.get("name", ""),
        "summary": metadata.get("description", ""),
        "dataset_link": metadata.get("url", ""),
        "authors": metadata.get("citeAs", ""),
        "publishing_organization": metadata.get("publisher", ""),
        "industry_types": [],
        "publishing_poc":  metadata.get("publishing_poc", {}),
        "dataset_owners": metadata.get("creator", {}),
        "dataset_authors": [metadata.get("citeAs", "")],
        "funding_sources": metadata.get("funding_sources", []),
        "data_subjects": metadata.get("data_subjects", []),
        "dataset_snapshot": {
            "Total Records": metadata.get("dataset_snapshot", {}).get("Total Records", ""),
            "Coverage": metadata.get("dataset_snapshot", {}).get("Coverage", ""),
            "Time Span": metadata.get("dataset_snapshot", {}).get("Time Span", "")
        },
        "content_description": metadata.get("content_description", ""),
        "descriptive_statistics": {
            "fields": metadata.get("descriptive_statistics", {}).get("fields", []),
            "stats": [
                {"name": stat.get("name", ""), "values": stat.get("values", [])}
                for stat in metadata.get("descriptive_statistics", {}).get("stats", [])
            ]
        },
        "sensitivity_types": metadata.get("sensitivity_types", []),
        "intentional_sensitive_data": [
            {"name": data.get("name", ""), "description": data.get("description", "")}
            for data in metadata.get("intentional_sensitive_data", [])
        ],
        "unintentional_sensitive_data": metadata.get("unintentional_sensitive_data", []),
        "security_privacy_handling": metadata.get("security_privacy_handling", ""),
        "risk_types": metadata.get("risk_types", []),
        "risks_mitigations": metadata.get("risks_mitigations", ""),
        "maintenance_status": metadata.get("maintenance_status", ""),
        "version_details": {
            "current_version": metadata.get("version_details", {}).get("current_version", ""),
            "last_updated": metadata.get("version_details", {}).get("last_updated", ""),
            "release_date": metadata.get("version_details", {}).get("release_date", "")
        },
        "maintenance_plan": metadata.get("maintenance_plan", ""),
        "next_update": {
            "version_affected": metadata.get("next_update", {}).get("version_affected", ""),
            "next_data_update": metadata.get("next_update", {}).get("next_data_update", ""),
            "next_version": metadata.get("next_update", {}).get("next_version", ""),
            "next_version_update": metadata.get("next_update", {}).get("next_version_update", "")
        },
        "expected_changes": metadata.get("expected_changes", ""),
        "primary_data_modality": metadata.get("primary_data_modality", ""),
        "sampling_data_points": [df.head().to_dict()],
        "data_fields": df.keys().tolist(),
        "typical_data_point": metadata.get("typical_data_point", "")
    }
    return dataset_info

def pretty_croissant_rai(metadata) -> dict:
    """
    Gets the ML Croissant metadata dict and returns another dict with our report format
    """
    dataset_info = {
        "dataCollection": metadata.get("dataCollection", ""),
        "dataCollectionType": metadata.get("dataCollectionType", ""),
        "dataCollectionRawData": metadata.get("dataCollectionRawData", ""),
        "dataAnnotationProtocol": metadata.get("dataAnnotationProtocol", ""),
        "dataAnnotationPlatform": metadata.get("dataAnnotationPlatform", ""),
        "dataAnnotationAnalysis": metadata.get("dataAnnotationAnalysis", ""),
        "dataUseCases": metadata.get("dataUseCases", ""),
        "dataBiases": metadata.get("dataBiases", ""),
        "annotationsPerItem": metadata.get("annotationsPerItem", ""),
        "annotatorDemographics": metadata.get("annotatorDemographics", "")
    }
    return dataset_info