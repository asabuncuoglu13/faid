# %%
import datetime
from yaml_utils import generate, update

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
    def init(project_name, config):
        """
        Initialize the fairness logging using the commonly used metadata tracking tools (wandb, mlflow, etc.)
        Takes a dictionary with the project name and configuration.
        project_name: str
        config: dictionary
        """
        init_metadata(project_name)
        update(config, "config")

    def log(metrics):
        """
        Log the fairness metrics
        metrics: a dictionary of metrics
        Returns: None - updates the metadata file, saves the data under the key 'metrics'
        """
        update(metrics, "metrics")

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
