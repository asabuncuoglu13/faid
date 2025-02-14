from os.path import join, exists
from shutil import copy
from datetime import datetime

from faid.logging import error_msg, warning_msg, success_msg, update, load, get_project_log_path, get_current_folder_path

exp_file_path = join(get_project_log_path(), "fairness.yml")
exp_file_template_path = join(get_current_folder_path(), "templates/fairness.yml")
exp_file_template_with_description_path = join(get_current_folder_path(), "template_example_descriptions/fairness_template_description.yml")

def initialize_exp_log(test:bool=False):
    if not exists(exp_file_path):
        if(test):
            copy(exp_file_template_with_description_path, exp_file_path)
            success_msg("Fairness experiment log created with sample descriptions.")
        else:
            copy(exp_file_template_path, exp_file_path)
            success_msg("Fairness experiment log created.")
    else:
        warning_msg("Fairness experiment log already exists. Logging will be appended to the existing file.")

def get_fairness_experiment_log_path():
    """
    Returns the path to the fairness log file
    """
    import os

    if os.path.exists(get_project_log_path()):
        fairness_files = [f for f in os.listdir(get_project_log_path()) if f.startswith('fairness_')]
        if len(fairness_files) == 1:
            return os.path.join(get_project_log_path(), fairness_files[0])
        else:
            return [os.path.join(get_project_log_path(), f) for f in fairness_files]
    else:
        import inquirer
        from IPython import get_ipython
        try:
            if 'IPKernelApp' in get_ipython().config:
                print("Enter the path to the fairness log file")
                fairness_log_filename = input()
                return fairness_log_filename
            else:
                raise ImportError
        except (ImportError, AttributeError):
            fairness_log_filename = inquirer.prompt([
                inquirer.List('input_file',
                                message='Select the log file',
                                choices=os.listdir('.'),
                                carousel=True)
            ])
        return fairness_log_filename['input_file']

def convert_experiment_filepath_format(filename:str) -> str:
    """
    Correct the filename
    """
    import re
    import os
    experiment_name = re.sub(r'[^\w\-_\. ]', '_', filename.replace(" ", "_").lower())
    experiment_file_name = os.path.join(get_project_log_path(), f"fairness_{experiment_name}.yml")
    return experiment_file_name

def get_exp_ctx(experiment_name:str) -> 'ExperimentContext':
    """
    Get the experiment context
    """
    dataDict = load(convert_experiment_filepath_format(experiment_name))

    return ExperimentContext(name=dataDict["name"], 
                                        context=dataDict["context"],
                                        data=dataDict["data"],
                                        sample_data=dataDict["sample_data"],
                                        model=dataDict["model"])

def pretty_aisi_summary(filepath:str) -> dict:
    import os
    import json
    filepath = os.path.join(os.getcwd(), filepath)
    if not os.path.exists(filepath):
        error_msg(f"{filepath} not found")
        return
    # read json filepath
    with open(filepath) as f:
        data = json.load(f)
    summary = {
        "name": data["eval"]["task_id"],
        "description": str(data["plan"]),
        "start_time": data["eval"]["created"],
        "data": data["eval"]["dataset"],
        "model": data["eval"]["model"],
        "metrics": {
            "total_samples": data["results"]["total_samples"],
            "completed_samples": data["results"]["completed_samples"],
            "scores": data["results"]["scores"]
            },
        "sample_results": data["results"]["sample_reductions"][0]["samples"][:5]
    }
    return summary

class ExperimentContext:
    """
    A class to represent an experiment context.
    """

    def __init__(self, name:str=None, 
                    context:dict=None,
                    data:dict=None,
                    sample_data:dict=None,
                    model:dict=None,
                    metrics:dict=None):

        if name is None:
            warning_msg("Please provide a name for the experiment")
            return

        self.name = name            
        self.filename = convert_experiment_filepath_format(name)
        
        if not exists(self.filename):
            copy(exp_file_template_path, self.filename)
            
        if context is None:
            context = load(self.filename)["context"]
        self.context = context

        if data is None:
            data = load(self.filename)["data"]
        self.data = data

        if sample_data is None:
            sample_data = load(self.filename)["sample_data"]
        self.sample_data = sample_data

        if model is None:
            model = load(self.filename)["model"]
        self.model = model

        if metrics is None:
            metrics = load(self.filename)["bias_metrics"]
        self.metrics = metrics

        self.metrics_schema = {'groups': 
                                {'group_name': '',
                                    'description': '',
                                    'label': '',
                                    'metrics': [
                                        {'name': '',
                                        'description': '',
                                        'value': 0,
                                        'threshold': 0,
                                        'bigger_is_better': False,
                                        'label': '',
                                        'notes': '',
                                        'sg_params': {}}]}}
        
        self.init_fairness_log()

    def init_fairness_log(self) -> dict:
        expCtx = load(self.filename)
        expCtx["name"] = self.name
        expCtx["context"] = self.context
        expCtx["data"] = self.data
        expCtx["sample_data"] = self.sample_data
        expCtx["model"] = self.model
        update(expCtx, filename=self.filename)
        return expCtx
        
    def to_dict(self):
        """Get a summary of the experiment."""
        metadata = {
            "name": self.name,
            "context": self.context,
            "data": self.data,
            "sample_data": self.sample_data,
            "model": self.model,
            "bias_metrics": self.metrics
        }
        return metadata
    
    def __str__(self):
        summary = self.to_dict()
        return "\n".join(f"{key}: {value}" for key, value in summary.items())

    def add_context_entry(self, key:str, entry):
        self.context = load(self.filename)["context"]
        self.context[key] = entry
        update(yaml_data=self.context, key="context", filename=self.filename)
        print(f"Added {key} to project metadata under ['context'] and log updated")

    def add_data_entry(self, key:str, entry):
        self.data = load(self.filename)["data"]
        self.data[key] = entry
        update(yaml_data=self.data, key="data", filename=self.filename)
        print(f"Added {key} to project metadata under ['data'] and log updated")
    
    def add_sample_data_entry(self, key:str, entry):
        self.sample_data = load(self.filename)["sample_data"]
        self.sample_data[key] = entry
        update(yaml_data=self.sample_data, key="sample_data", filename=self.filename)
        print(f"Added {key} to project metadata under ['sample_data'] and log updated")
    
    def add_model_entry(self, key:str, entry):
        self.model = load(self.filename)["model"]
        self.model[key] = entry
        update(yaml_data=self.model, key="model", filename=self.filename)
        print(f"Added {key} to project metadata under ['model'] and log updated")
    
    def add_metric_entry(self, entry:dict={}):
        self.metrics = load(self.filename)["bias_metrics"]
        if entry == {}:
            error_msg("Please provide an entry to add")
            return
        if entry.keys() != self.metrics_schema.keys():
            error_msg("Entry does not comply with the metrics schema. Call .metrics_schema to see the schema.")
            return
        self.metrics = entry
        update(yaml_data=self.metrics, key="bias_metrics", filename=self.filename)
        print("Added the metrics to project metadata under ['bias_metrics'] and log updated")

    def get_metric_entry(self, key:str=None):
        if key is None:
            return self.metrics
        if self.metrics.get(key, None) is None:
            return self.metrics.get("groups").get(key, None)
        return self.metrics.get(key, None)

    def add_entry(self, entry):
        from captum.attr import visualization as viz
        if isinstance(entry, viz.VisualizationDataRecord):
            entry_dict = {
                "word_attributions": entry.word_attributions.detach().cpu().numpy().tolist() if hasattr(entry.word_attributions, 'detach') else entry.word_attributions,
                "pred_prob": entry.pred_prob.detach().cpu().numpy().tolist() if hasattr(entry.pred_prob, 'detach') else entry.pred_prob,
                "pred_class": entry.pred_class.detach().cpu().numpy().tolist() if hasattr(entry.pred_class, 'detach') else entry.pred_class,
                "true_class": entry.true_class.detach().cpu().numpy().tolist() if hasattr(entry.true_class, 'detach') else entry.true_class,
                "attr_class": entry.attr_class.detach().cpu().numpy().tolist() if hasattr(entry.attr_class, 'detach') else entry.attr_class,
                "attr_score": entry.attr_score.detach().cpu().numpy().tolist() if hasattr(entry.attr_score, 'detach') else entry.attr_score,
                "raw_input_ids": entry.raw_input_ids.detach().cpu().numpy().tolist() if hasattr(entry.raw_input_ids, 'detach') else entry.raw_input_ids,
                "convergence_score": entry.convergence_score.detach().cpu().numpy().tolist() if hasattr(entry.convergence_score, 'detach') else entry.convergence_score,
            }
            self.add_model_entry("captum_records", entry_dict)

    def set_context(self, 
            description:str="", 
            start_time:str=None, 
            tags:list=[],
            authors:list=[],
            hardware:dict={},
            license_info:list=[]):
        self.description = description
        if start_time is None:
            start_time = datetime.now().isoformat()
        self.context.start_time = start_time
        self.context.tags = tags
        self.context.authors = authors
        self.context.hardware = hardware
        self.context.license_info = license_info

        expCtx = load(self.filename)["context"]
        expCtx["description"] = self.description
        expCtx["start_time"] = self.context.start_time
        expCtx["tags"] = self.context.tags
        expCtx["authors"] = self.context.authors
        expCtx["hardware"] = self.context.hardware
        update(yaml_data=expCtx, key="context", filename=self.filename)


    def get_context_entry(self, key:str=None):
        if key is None:
            return self.context
        return self.context.get(key, None)

    def get_data_entry(self, key:str=None):
        if key is None:
            return self.data
        return self.data.get(key, None)
    
    def get_sample_data_entry(self, key:str=None):
        if key is None:
            return self.sample_data
        return self.sample_data.get(key, None)
    
    def get_model_entry(self, key:str=None):
        if key is None:
            return self.model
        return self.model.get(key, None)