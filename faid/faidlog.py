# %%
import datetime
from .utils.logging.yaml_utils import generate, update
from .utils.logging.model_card_utils import ModelCard

# %%
def init_metadata(project_name, author=None, date=None, description=None, version=None):
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

# %%
class faidlog:
    """
    A class to log fairness metrics.
    """
    @staticmethod
    def init(project_name:str, config:dict):
        """
        Initialize the fairness logging using the commonly used metadata tracking tools (wandb, mlflow, etc.)
        Takes a dictionary with the project name and configuration.
        project_name: str
        config: dictionary
        """
        init_metadata(project_name)
        update(config, "config")
    
    @staticmethod
    def log(params:dict, key:str="metrics", add_to_model_card=False, add_to_fairness_report=False, add_to_data_card=False, add_to_risk_register=False):
        """
        Log the fairness metrics
        params: Any value that can be stored in a dictionary
        key: str - the key to store the data under in the metadata file
        Returns: None - updates the metadata file
        """
        if add_to_model_card:
            update(params, key, "model")
        elif add_to_fairness_report:
            update(params, key, "fairness")
        elif add_to_data_card:
            update(params, key, "data")
        elif add_to_risk_register:
            update(params, key, "risk")
        else:
            update(params, key)

    @staticmethod
    def model_info(info: ModelCard):
        info = info.get_model_info()
        update(info, "model_info")

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
