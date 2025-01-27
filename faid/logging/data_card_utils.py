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

def get_data_entry(key:str):
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
        "version_details": metadata.get("content_description", ""),
        "sampling_data_points": [df.head().to_dict()],
        "data_fields": df.keys().tolist()
    }

def pretty_croissant_rai(metadata) -> dict:
    """
    Gets the ML Croissant metadata dict and returns another dict with our report format
    """
    return {
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

def pretty_uci_metadata(metadata) -> dict:
    """
    Gets the UCI metadata dict and returns another dict with our report format
    """
    return {
        "id": metadata.get("uci_id", ""),
        "dataset_name": metadata.get("name", ""),
        "repository_url": metadata.get("repository_url", ""),
        "dataset_link": metadata.get("data_url", ""),
        "summary": metadata.get("abstract", ""),
        "industry_types": metadata.get("area", ""),
        "tasks": metadata.get("tasks", []),
        "characteristics": metadata.get("characteristics", []),
        "num_instances": metadata.get("num_instances", ""),
        "num_features": metadata.get("num_features", ""),
        "feature_types": metadata.get("feature_types", []),
        "protected_characteristics": metadata.get("demographics", ""),
        "target_col": metadata.get("target_col", ""),
        "index_col": metadata.get("index_col", ""),
        "has_missing_values": metadata.get("has_missing_values", False),
        "missing_values_symbol": metadata.get("missing_values_symbol", ""),
        "version_details": {
            "current_version": "",
            "last_updated": metadata.get("last_updated", ""),
            "release_date": metadata.get("year_of_dataset_creation", "")
        },
        "authors": metadata.get("creators", []),
        "intro_paper": metadata.get("intro_paper", ""),
        "funding_sources": metadata.get("additional_info", "").get("funded_by", ""),
        "intentional_sensitive_data": metadata.get("additional_info", "").get("sensitive_data", ""),
        "data_fields": metadata.get("additional_info", "").get("variable_info", []),
    }