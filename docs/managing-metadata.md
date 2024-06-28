# Managing Metadata

There are multiple ways/tools/systems to define metadata. If you use some of the popular experiment tracking or CI/CD tools, you are probably familiar with experiment parameters and storing them.

The below example demonstrates how you can config a FAID monitoring log if you are already using Weights & Biases (W&B):

```python
import wandb
from faid import faidlog

# Define a config dictionary object

@faidlog.config
config = {
    "hidden_layer_sizes": [32, 64],
    "kernel_sizes": [3],
    "activation": "ReLU",
    "pool_sizes": [2],
    "dropout": 0.5,
    "num_classes": 10,
}

# Pass the config dictionary when you initialise W&B and initiliase faidlog with the same project name
@faidlog.init
run = wandb.init(project="fairness_monitoring_example", config=config)

# Alternatively, if you want to use different project name:
# faidlog.init(project="fairness_monitoring_alternative_example")

...
# You can access values from this config dict i.e.:
hidden_layer_sizes = wandb.config["hidden_layer_sizes"]

...
# And log inside the training function for the updated variables
@faidlog.params
wandb.log({
    "epoch": epoch,
    "train_acc": train_acc,
    "train_loss": train_loss,
    "val_acc": val_acc,
    "val_loss": val_loss,
})
```

After the running your experiment, you will see the below output config under the ```logs``` folder with the specified project_name, and date_time (e.g. ```fairness_monitoring_example_20240627_152203.yml```)

```yml

project:
    name: "fairness_monitoring_example"

experiment:
    seed: 20240627

train:
    data:
        split: 0.20
    parameters:
        epoch: 10
        batch_size: 32
        optimizer: Adam
        activation: ReLU
        lr: 0.001
```

## Adding more experiment results

After the experiment metadata file is initiated with the config parameters, you can add any experiment log, parameter as you wish. For example, let's say after the data profiling, you can add some of the useful information to replicate the experiments:

```python
import json
from ydata_profiling import ProfileReport
profile = ProfileReport(raw_data, title="Profiling Report")
data = json.loads(profile.to_json())

profile_save_results = {
    "variables": data["variables"].keys(),
    "number_of_observations": data["table"]["n"]
    "missing_cells": data["table"]["n_cells_missing"]
    "duplicate rows": data["table"]["n_duplicates"]
}

```

It is not recommended, but, alternatively, you can save the entire profiling JSON file:
```python
json_data = profile.to_json()
faidlog.log("data_profile", json_data) # This will automatically convert the string to JSON object and add all elements to the YAML file.
```
Since the profile JSON holds many information, including the complete data, we do not recommend saving it to the fairness monitoring metadata due to the performance reasons.


The resulted YAML file will look like this:

```yml

project:
    name: "fairness_monitoring_example"

experiment:
    seed: 20240627

data_profile:
    variables: ['sentiment', 'text']
    number_of_observations: 4846
    missing_cells: 0
    duplicate rows: 6

train:
    data:
        split: 0.20
    parameters:
        epoch: 10
        batch_size: 32
        optimizer: Adam
        activation: ReLU
        lr: 0.001
```

Or, let's say you want to use fairlearn library. You can add all the fairness metric scores in a dict object and log it to the monitoring metadata.

```python
fairness_metrics = {
    "balanced_accuracy": balanced_accuracy_score,
    "false_positive_rate": false_positive_rate,
    "false_negative_rate": false_negative_rate,

    "false_negative_error": false_negative_error,
}
faidlog.log("fairness_metrics", fairness_metrics)
```

The resulted YAML file will look like this:

```yml

project:
    name: "fairness_monitoring_example"

experiment:
    seed: 20240627

data_profile:
    variables: ['sentiment', 'text']
    number_of_observations: 4846
    missing_cells: 0
    duplicate rows: 6

train:
    data:
        split: 0.20
    parameters:
        epoch: 10
        batch_size: 32
        optimizer: Adam
        activation: ReLU
        lr: 0.001

fairness_metrics:
    balanced_accuracy: 0.801682
    false_positive_rate: 0.207656
    false_negative_rate: 0.188980
```
