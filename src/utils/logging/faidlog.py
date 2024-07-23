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
            update({"config": config})
        else:
            error_msg("The object provided is not a wandb run object.")


"""
class faidlog:
    @staticmethod
    def init(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extracting 'project' and 'config' from kwargs
            project = kwargs.get('project')
            config = kwargs.get('config')
            
            if not project or not config:
                raise ValueError("Both 'project' and 'config' must be provided.")
            
            init_metadata(project)
            update({"config": config})
            
            # Execute the original function
            return func(*args, **kwargs)
        
        return wrapper
"""  
"""
class faidlog:
    @staticmethod
    def init(func):
        @functools.wraps(func)
        def wrapper():
            # Execute the original function
            run = func()

            # Extracting 'project' and 'config' from kwargs
            project = run.project
            config = run.config.as_dict()
            
            if not project or not config:
                raise ValueError("Both 'project' and 'config' must be provided.")
            
            init_metadata(project)
            update(config, key="config")
            
        return wrapper

# Example usage
@faidlog.init
def init_wandb():
    return wandb.init(
        # set the wandb project where this run will be logged
        project= project,
        # track hyperparameters and run metadata
        config= config
    )

init_wandb()
"""
# %% Example usage
import random

project = "test-project-1"
config = {
    "learning_rate": 0.02,
    "architecture": "CNN",
    "dataset": "CIFAR-100",
    "epochs": 10,
}

# %%
run = wandb.init(project= project, config= config)
faidlog.init(run)

# %% simulate training
epochs = 10
offset = random.random() / 5
for epoch in range(2, epochs):
    acc = 1 - 2 ** -epoch - random.random() / epoch - offset
    loss = 2 ** -epoch + random.random() / epoch + offset

    # log metrics to wandb
    wandb.log({"acc": acc, "loss": loss})

# [optional] finish the wandb run, necessary in notebooks
wandb.finish()