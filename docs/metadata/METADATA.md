# Managing Log Data using Python

When you develop a program, all the tooling generates some kind of log. Sometimes, you don't care what the log is, sometimes you spend hours to decode what the log says. Experiment logging is a common practice in ML development. Developing a model is not cheap; it can cost up to millions of dollars. So, in most cases, developers should squeeze every information they could get from one single experiment. 

For example, let's consider the scenario, where you are already using Weights & Biases (W&B). Your interaction with the log generally looks like the following code snippet:

```python
import wandb

# Define a config dictionary object
config = {
    "hidden_layer_sizes": [32, 64],
    "kernel_sizes": [3],
    "activation": "ReLU",
    "pool_sizes": [2],
    "dropout": 0.5,
    "num_classes": 10,
}

# Pass the config dictionary when you initialise W&B and initiliase faidlog with the same project name
run = wandb.init(project="fairness_monitoring_example", config=config)

...
# You can access values from this config dict i.e.:
hidden_layer_sizes = wandb.config["hidden_layer_sizes"]

...
# And log inside the training function for the updated variables
training_data = {
    "epoch": epoch,
    "train_acc": train_acc,
    "train_loss": train_loss,
    "val_acc": val_acc,
    "val_loss": val_loss,
    "roc_auc": roc_auc
}

wandb.log(training_data)
```

## Update Model Metadata

If this model training results are the latest ones for the deployed model, sync this information with `model.yml` file.

You can do it by generating a `ModelCard` object and saving it as project metadata:

```python
from faid.logging import ModelCard
m = ModelCard()
m.set_model_parameters(config, keyword="model_architecture")
m.add_quantitative_analysis_metric({
    'name': 'ROC AUC Score',
    'description': 'ROC AUC Score is the area under the ROC curve',
    'value': roc_auc,
    ... # other fields
})
```

As you can realise, FAID incentives adding details like description, and promotes a much more structured logging process. Because the goal is communicating these results as much stakeholders as possible.


## Update Data Metadata

After the experiment metadata file is initiated with the config parameters, you can add any experiment log, parameter as you wish. For example, let's say after the data profiling, you can add some of the useful information to replicate the experiments:

```python
import json
from ydata_profiling import ProfileReport
from faid import logging as faidlog

profile = ProfileReport(raw_data, title="Profiling Report")
data = json.loads(profile.to_json())

faidlog.add_data_entry(key="variables", entry=data["variables"].keys())
faidlog.add_data_entry(key="number_of_observations", entry=data["table"]["n"])
faidlog.add_data_entry(key="missing_cells", entry=data["table"]["n_cells_missing"])
faidlog.add_data_entry(key="duplicate rows", entry=data["table"]["n_duplicates"])
```

## Update Fairness Metadata
FAID expects you to follow a standard recording format in fairness metric reporting. Although it will not generate an error, it will be unhappy about it and will warn you. You can use Fairness Metrics Ontology (<https://github.com/frankj-rpi/fairness-metrics-ontology/tree/main>) as the standard relational map of fairness notions and metrics.

Let's say, you want to record statistical parity difference. The resulting YAML file should look like this:

```yaml
name: "statistical parity difference"
description: "Statistical parity difference is the difference in approval rates between two groups."
value: -0.108
threshold: 0 # 0 indicates perfect fairness, select this value based on your business case, regulatory requirements, and statistical significance.
bigger_is_better: false
label: "statistical_parity_difference"
notes: ""
sg_params: {} # we don't have any additonal subgroups in this case
```

To include your statistical parity difference testing, first you need to create an a `FairnessExperimentRecord`, than save the bias metric. Note that bias metric should be recorded under a `group`. As all fairness testing is about being fair among "priviliged" and "unpriviliged" groups (e.g. male, female), recording follows this scheme.

```python
from faid import logging as faidlog
experiment_name = "credit-scoring-default"
fairness_experiment = faidlog.FairnessExperimentRecord(experiment_name)
...
# The following code creates a metric frame using the fairness metrics included in fairlearn library
metricframe_unmitigated = MetricFrame(
    metrics=fairness_metrics,
    y_true=y_test,
    y_pred=Y_pred,
    sensitive_features=A_test,
)
...
# Record the fairlearn's metric frame
grouped_metrics = metricframe_unmitigated.by_group
fairness_experiment.add_metric_entry(key="unmitigated_sex_group_metrics", entry=grouped_metrics.to_dict())    
```
