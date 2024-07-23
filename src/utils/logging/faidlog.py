# %%
import datetime
import wandb
from yaml_utils import generate, update
from message import error_msg

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
    def init(initObj):
        if  isinstance(initObj, wandb.sdk.wandb_run.Run):
            project = initObj.project
            config = initObj.config.as_dict()
            init_metadata(project)
            update(config, "config")
        else:
            error_msg("The object provided is not a wandb run object.")

    def log(metrics):
        update(metrics, "metrics")

# %% Example usage
"""
import random
project = "test-project-1"
config = {
    "learning_rate": 0.02,
    "architecture": "CNN",
    "dataset": "CIFAR-100",
    "epochs": 10,
}

# initialize wandb run
run = wandb.init(project= project, config= config)
faidlog.init(run)

# simulate training
epochs = 10
offset = random.random() / 5
for epoch in range(2, epochs):
    acc = 1 - 2 ** -epoch - random.random() / epoch - offset
    loss = 2 ** -epoch + random.random() / epoch + offset

    # log metrics to wandb
    metrics = {"acc": acc, "loss": loss}
    wandb.log(metrics)
    faidlog.log(metrics)

# [optional] finish the wandb run, necessary in notebooks
wandb.finish()
"""