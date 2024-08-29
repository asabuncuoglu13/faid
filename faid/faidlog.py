# %%
import datetime
from .logging.yaml_utils import generate, update, load
from .logging.message import error_msg
from .logging.model_card_utils import ModelCard
from .report.report_utils import generate_data_card, generate_fairness_report, generate_model_card, generate_raid_register_report

# %%
class faidlog:
    """
    A class to log fairness metrics.
    """

    files ={        
        "fairness_yml_file": "fairness",
        "model_yml_file": "model",
        "data_yml_file": "data",
        "risk_yml_file": "risks",
    }
    
    keys = {
        "config_key": "config",
        "model_info_key": "model_info",
        "sample_data_key" : "sample_results"
    }

    @staticmethod
    def __str__() -> str:
        print("Fairness Logging")
        return "Fairness Logging"

    @staticmethod
    def init_project(project_name:str, author:str=None, date:str=None, description:str=None, version:str=None):
        """
        Initialize the metadata
        """
        metadata = {
            "project": project_name,
            "author": author if author else "Author",
            "date": date if date else datetime.date.today().isoformat(),
            "description": description if description else "",
            "version": version if version else "0.1.0"
        }
        generate(metadata)
        return metadata  # Return the metadata dictionary

    @staticmethod
    def init_project_with_config(project_name:str, config:dict):
        """
        Initialize the fairness logging using the commonly used metadata tracking tools (wandb, mlflow, etc.)
        Takes a dictionary with the project name and configuration.
        project_name: str
        config: dictionary
        """
        generate({
            "project": project_name,
            faidlog.keys["config_key"]: config
        })  
    
    @staticmethod
    def log(params:dict, key:str, add_to_model_card:bool=False, add_to_fairness_report:bool=False, add_to_data_card:bool=False, add_to_risk_register:bool=False):
        """
        Log the fairness metrics
        params: Any value that can be stored in a dictionary
        key: str - the key to store the data under in the metadata file
        Returns: None - updates the metadata file
        """
        if add_to_model_card:
            update(params, key=key, filename=faidlog.files["model_yml_file"])
            print(f"Added {key} to model card")
        elif add_to_fairness_report:
            update(params, key=key, filename=faidlog.files["fairness_yml_file"])
            print(f"Added {key} to fairness report")
        elif add_to_data_card:
            update(params, key=key, filename=faidlog.files["data_yml_file"])
            print(f"Added {key} to data card")
        elif add_to_risk_register:
            update(params, key=key, filename=faidlog.files["risk_yml_file"])
            print(f"Added {key} to risk register")
        else:
            update(params, key=key)
            print(f"Added {key} to project metadata")

    @staticmethod
    def generate_all_reports():
        """
        Generate all the reports
        """
        #generate_model_card()
        generate_data_card()
        generate_fairness_report()
        generate_raid_register_report()
        print("All reports generated")

    @staticmethod
    def model_info(info: ModelCard):
        info = info.get_model_info()
        update(info, key=faidlog.keys["model_info_key"])

    @staticmethod
    def get(key:str, from_fairness_report=False, from_model_card=False, from_data_card=False, from_risk_register=False):
        """
        Get the metadata
        """
        if from_fairness_report:
            data = load(faidlog.files["fairness_yml_file"])
        elif from_model_card:
            data = load(faidlog.files["model_yml_file"])
        elif from_data_card:
            data = load(faidlog.files["data_yml_file"])
        elif from_risk_register:
            data = load(faidlog.files["risk_yml_file"])
        else:  
            data = load()

        try:
            val = data[key]
            return val
        except KeyError:
            error_msg(f"Key {key} not found in the metadata file")
            return None
    
    @staticmethod
    def get_fairness_data():
        return load(faidlog.files["fairness_yml_file"])
    
    @staticmethod
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



# %% Example usage
"""
import random
import wandb
import mlflow

project = "test-project-1"
config = {
    "learning_rate": 0.02,
    "architecture": "CNN",
    "dataset": "CIFAR-100",
    "epochs": 10,
}

# initialize wandb run
run = wandb.init(project= project, config= config)
mlflow.set_experiment(project)
faidlog.init(project_name= project, config= config)

with mlflow.start_run():
    # Log the hyperparameters
    # simulate training
    epochs = 10
    offset = random.random() / 5
    for epoch in range(2, epochs):
        acc = 1 - 2 ** -epoch - random.random() / epoch - offset
        loss = 2 ** -epoch + random.random() / epoch + offset

        # log metrics to wandb
        metrics = {"acc": acc, "loss": loss}
        wandb.log(metrics)
        mlflow.log_params(metrics)
        faidlog.log(metrics)

# [optional] finish the wandb run, necessary in notebooks
wandb.finish()
"""
# %%
