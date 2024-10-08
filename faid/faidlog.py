# %%
import sys
import os
import pkg_resources
from datetime import datetime
from .logging.yaml_utils import update, load, get_project_log_path
from .logging.message import error_msg
from .report.report_utils import generate_data_card, generate_model_card, generate_raid_register_report, generate_experiment_overview_report, generate_transparency_report

# %%
class faidlog:
    """
    A class to log fairness metrics.
    """

    @staticmethod
    def get_current_folder_path():
        import os
        return os.path.dirname(os.path.abspath(__file__))

    files ={
        "model_yml_file": os.path.join(get_project_log_path(), "model.yml"),
        "data_yml_file": os.path.join(get_project_log_path(),"data.yml"),
        "risk_yml_file": os.path.join(get_project_log_path(),"risks.yml"),
        "transparency_yml_file": os.path.join(get_project_log_path(), "transparency.yml")
    }
    
    keys = {
        "config_key": "config",
        "model_info_key": "model_info",
        "sample_data_key" : "sample_results"
    }
    
    templates = {
        "fairness_template": os.path.join(get_current_folder_path(), "logging/templates/fairness.yml"),
        "model_template": os.path.join(get_current_folder_path(), "logging/templates/model.yml"),
        "data_template": os.path.join(get_current_folder_path(), "logging/templates/data.yml"),
        "risk_template": os.path.join(get_current_folder_path(), "logging/templates/risks.yml"),
        "transparency_template": os.path.join(get_current_folder_path(), "logging/templates/transparency.yml")
    }

    @staticmethod
    def __str__() -> str:
        print("Fairness Logging")
        return "Fairness Logging"
    
    @staticmethod
    def init():
        # create a log directory if it does not exist
        import os
        if not os.path.exists(get_project_log_path()):
            os.makedirs(get_project_log_path())

        # copy the template files to the log directory
        import shutil
        
        if not os.path.exists(faidlog.files["model_yml_file"]):
            shutil.copy(faidlog.templates["model_template"], faidlog.files["model_yml_file"])
        else:
            print("Model log file already exists")
        if not os.path.exists(faidlog.files["data_yml_file"]):
            shutil.copy(faidlog.templates["data_template"], faidlog.files["data_yml_file"])
        else:
            print("Data log file already exists")
        if not os.path.exists(faidlog.files["risk_yml_file"]):
            shutil.copy(faidlog.templates["risk_template"], faidlog.files["risk_yml_file"])
        else:
            print("Risk log file already exists")
        if not os.path.exists(faidlog.files["transparency_yml_file"]):
            shutil.copy(faidlog.templates["transparency_template"], faidlog.files["transparency_yml_file"])
        else:
            print("Transparency log file already exists")
        
        print("Logging initialized")
    
    @staticmethod
    def convert_experiment_filepath_format(filename:str) -> str:
        """
        Correct the filename
        """
        import re
        import os
        experiment_name = re.sub(r'[^\w\-_\. ]', '_', filename.replace(" ", "_").lower())
        experiment_file_name = os.path.join(get_project_log_path(), f"fairness_{experiment_name}.yml")
        return experiment_file_name
    
    @staticmethod
    def add_model_entry(params:dict, key:str="model_info"):
        update(params, key=key, filename=faidlog.files["model_yml_file"])
        print(f"Added {key} to model card")

    @staticmethod
    def get_model_entry(key:str=None):
        if key is None:
            return load(faidlog.files["model_yml_file"])
        else:
            try:
                return load(faidlog.files["model_yml_file"])[key]
            except KeyError:
                error_msg(f"Key {key} not found in the metadata file")
                return None

    @staticmethod
    def add_data_entry(entry:dict, key:str="dataset_info"):
        """
        Add a data entry to the data card
        """
        try:
            if entry.get("conformsTo") == 'http://mlcommons.org/croissant/RAI/1.0':
                key="rai"
        except AttributeError | KeyError:
            pass
        update(entry, key=key, filename=faidlog.files["data_yml_file"])
        print(f"Added {key} to data card")

    @staticmethod
    def get_data_entry(key:str=None):
        if key is None:
            return load(faidlog.files["data_yml_file"])
        else:
            try:
                return load(faidlog.files["data_yml_file"])[key]
            except KeyError:
                error_msg(f"Key {key} not found in the metadata file")
                return None
    
    @staticmethod
    def add_risk_entry(params:dict, key:str="risks"):
        """
        Add a risk entry to the risk register
        Key can be one of ["risks", "assumptions", "issues", "dependencies"]
        """
        keys = ["risks", "assumptions", "issues", "dependencies"]
        if key not in keys:
            error_msg(f"Key {key} not found in the metadata file. Please use one of {keys}")
            return None
        
        # add an id to the risk entry
        risk_data = load(faidlog.files["risk_yml_file"])
        id = len(risk_data[key]) + 1

        update({id: params}, key=key, filename=faidlog.files["risk_yml_file"])
        print(f"Added {key} to risk register")
    
    @staticmethod
    def get_risk_entry(key:str=None):
        if key is None:
            return load(faidlog.files["risk_yml_file"])
        else:
            try:
                return load(faidlog.files["risk_yml_file"])[key]
            except KeyError:
                error_msg(f"Key {key} not found in the metadata file")
                return None

    @staticmethod
    def add_transparency_entry(params:dict, key:str="transparency_info"):
        update(params, key=key, filename=faidlog.files["transparency_yml_file"])
        print(f"Added {key} to transparency metadata")
    
    @staticmethod
    def get_transparency_entry(key:str=None):
        if key is None:
            return load(faidlog.files["transparency_yml_file"])
        else:
            try:
                return load(faidlog.files["transparency_yml_file"])[key]
            except KeyError:
                error_msg(f"Key {key} not found in the metadata file")
                return None
            

    @staticmethod
    def get_fairness_log_path():
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

    @staticmethod
    def generate_experiment_overview_report(project_info:dict=None):
        """
        Generate the project overview report
        """
        # for each file starts with fairness_, generate the report
        if project_info is None:
            fairness_files = faidlog.get_fairness_log_path()
            if isinstance(fairness_files, list):
                for file in fairness_files:
                    project_info = load(file)
                    generate_experiment_overview_report(project_info)
            else:
                project_info = load(fairness_files)
                generate_experiment_overview_report(project_info)

    @staticmethod
    def generate_model_card_report(custom_file_path:str=None):
        """
        Generate the model card report
        """
        import os
        if not os.path.exists(faidlog.files["model_yml_file"]):
            print("Model log file not found")
            return
        else:
            if custom_file_path is None:
                generate_model_card()
            else:
                if os.path.exists(custom_file_path):
                    info = load(custom_file_path)
                    generate_model_card(model_info=info)
                else:
                    print("Custom file path not found")

    @staticmethod
    def generate_data_card_report(input_file_path:str=None, output_file_path:str=None):
        """
        Generate the data card report
        """
        import os
        if input_file_path is not None:
            if os.path.exists(input_file_path):
                info = load(input_file_path)
            else:
                print("Input file path not found")
        else:
            info = faidlog.get_data_entry()
            if not os.path.exists(faidlog.files["data_yml_file"]):
                print("Data log file not found")
                return
            else:
                if output_file_path is not None:
                    generate_data_card(dataset_info=info, output_file=output_file_path)
                else:
                    generate_data_card(dataset_info=info)
    
    @staticmethod
    def generate_transparency_report(custom_file_path:str=None):
        """
        Generate the transparency report
        """
        import os
        if not os.path.exists(faidlog.files["transparency_yml_file"]):
            print("Transparency log file not found")
            return
        else:
            if custom_file_path is None:
                generate_transparency_report()
            else:
                if os.path.exists(custom_file_path):
                    info = load(custom_file_path)
                    generate_transparency_report(transparency_data=info)
                else:
                    print("Custom file path not found")

    @staticmethod
    def generate_risk_register_report(custom_file_path:str=None):
        """
        Generate the risk register report
        """
        import os
        if not os.path.exists(faidlog.files["risk_yml_file"]):
            print("Risk log file not found")
            return
        else:
            if custom_file_path is None:
                generate_raid_register_report()
            else:
                if os.path.exists(custom_file_path):
                    info = load(custom_file_path)
                    generate_raid_register_report(risk_data=info)
                else:
                    print("Custom file path not found")

    @staticmethod
    def generate_all_reports():
        """
        Generate all the reports
        """
        faidlog.generate_experiment_overview_report()
        faidlog.generate_model_card_report()
        faidlog.generate_data_card_report()
        faidlog.generate_risk_register_report()
        print("All reports generated")
    
    @staticmethod
    def get_fairness_entry(key:str=None):
        if key is None:
            return load(faidlog.get_fairness_log_path())
        else:
            try:
                return load(faidlog.get_fairness_log_path())[key]
            except KeyError:
                error_msg(f"Key {key} not found in the metadata file")
                return None
    
    @staticmethod
    def generate_fairness_log_completeness_label():
        """
        Generate a digital trust label as SVG and add it to the reports/README.md file.
        """
        import os
        import svg

        def calculate_log_completeness(log_path):
            """
            Calculate the completeness of fairness logs.

            Args:
            log_path: The path to the fairness log file.

            Returns:
            A float between 0 and 1 representing the completeness of fairness logs,
            where 1 is fully complete.
            """
            fairness_log_keys = ["sample_results", "variable_profile", "bygroup_metrics"]  # Define the expected fairness log keys
            fairness_log = load(log_path)
            fairness_log_keys_found = [key for key in fairness_log.keys() if key in fairness_log_keys]
            log_completeness = len(fairness_log_keys_found) / len(fairness_log_keys)
            print(f"We found the keys: {str(fairness_log_keys_found)}. Based on the log, the fairness log completeness is calculated: {log_completeness}")
            return log_completeness

        def generate_fairness_logo(log_completeness, output_filename="fairness_logo.svg"):
            """
            Generates an SVG fairness certification logo with dynamic color and shape
            based on the completeness of fairness logs.

            Args:
            log_completeness: A float between 0 and 1 representing the completeness
                    of the fairness logs, where 1 is fully complete.
            output_filename: The name of the SVG file to save the logo.

            Returns:
            None. Saves the generated logo to an SVG file.
            """

            # Color Mapping (Example):
            hue = 270  # Hue for purple
            saturation = int(100 * log_completeness)  # Saturation based on log completeness
            lightness = 50  # Fixed lightness
            color_hsl = f'hsl({hue}, {saturation}%, {lightness}%)'

            canvas = svg.SVG(
                width=100, 
                height=100,
                elements = [
                    svg.Circle(cx=50, cy=50, r=40 * log_completeness, fill=color_hsl, stroke='black', stroke_width=2)
                ]
            )
            
            with open(output_filename, 'w') as f:
                f.write(str(canvas))
            return canvas
        
        def add_label_to_readme(fairness_logo):
            """
            Add the fairness logo to the README file.
            """
            readme_file = "reports/README.md"
            if not os.path.exists(readme_file):
                with open(readme_file, 'w') as f:
                    f.write("# Fairness Report Overview\n\n")
                    f.write("This README contains the fairness report and related information.\n\n")

            with open(readme_file, 'a') as f:
                f.write(str(fairness_logo))
            return
        
        log_path = faidlog.get_fairness_log_path()
        log_completeness = calculate_log_completeness(log_path)
        fairness_logo = generate_fairness_logo(log_completeness)
        add_label_to_readme(fairness_logo)
        return

    @staticmethod
    def pretty_aisi_summary(filepath:str) -> dict:
        import os
        import json
        filepath = os.path.join(os.getcwd(), filepath)
        if not os.path.exists(filepath):
            print(f"{filepath} not found")
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
    
    @staticmethod
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
    
    @staticmethod
    def get_imported_libraries():
        # Get all imported modules
        imported_modules = [m.__name__ for m in sys.modules.values() if m]
        # include only modules that are not in the standard library
        imported_modules = [m for m in imported_modules if m not in sys.builtin_module_names]
        # remove module submodules
        imported_modules = [m.split('.')[0] for m in imported_modules]
        # remove duplicates
        imported_modules = list(set(imported_modules))
        
        # Get the version of each imported module if available
        modules_with_versions = {}
        for module_name in imported_modules:
            # if module_name does not start with _
            if module_name.startswith('_'):
                continue
            try:
                version = pkg_resources.get_distribution(module_name).version
                modules_with_versions[module_name] = version
            except pkg_resources.DistributionNotFound:
                pass
        
        return sorted(modules_with_versions.items())
    
    @staticmethod
    def get_package_licenses():
        import importlib.metadata
        root = os.getcwd()
        with open(os.path.join(root, 'requirements.txt'), 'r') as f:
            packages = f.read().splitlines()
            packages = [pkg.split('==')[0] for pkg in packages if pkg]
            try:
                licenses = []
                for package in packages:
                    metadata = importlib.metadata.metadata(package)
                    license = metadata.get('License')
                    if not license:
                        license = metadata.get('Classifier', [])
                        license_info = [line for line in license if line.startswith('License')]
                        license = license_info[0] if license_info else 'License information not found'
                    licenses.append((package, license))
            except importlib.metadata.PackageNotFoundError:
                licenses.append((package, "Package not found")) 
        return licenses

    @staticmethod
    def get_ctx(experiment_name:str) -> 'ExperimentContext':
        """
        Get the experiment context
        """
        dataDict = load(faidlog.convert_experiment_filepath_format(experiment_name))

        return faidlog.ExperimentContext(name=dataDict["name"], 
                                         context=dataDict["context"],
                                         data=dataDict["data"],
                                         sample_data=dataDict["sample_data"],
                                         model=dataDict["model"])
    
    class ExperimentContext:
        """
        A class to represent an experiment context.
        """

        def __init__(self, name:str=None, 
                     context:dict=None,
                     data:dict=None,
                     sample_data:dict=None,
                     model:dict=None):
            import os
            import shutil

            if name is None:
                print("Please provide a name for the experiment")
                return

            self.name = name            
            self.filename = faidlog.convert_experiment_filepath_format(name)
            
            if not os.path.exists(self.filename):
                shutil.copy(faidlog.templates["fairness_template"], self.filename)
                
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
            }
            return metadata
        
        def __str__(self):
            summary = self.to_dict()
            return "\n".join(f"{key}: {value}" for key, value in summary.items())

        def add_context_entry(self, key:str, entry):
            self.context = load(self.filename)["context"]
            self.context[key] = entry
            update(yamlData=self.context, key="context", filename=self.filename)
            print(f"Added {key} to project metadata under ['context'] and log updated")

        def add_data_entry(self, key:str, entry):
            self.data = load(self.filename)["data"]
            self.data[key] = entry
            update(yamlData=self.data, key="data", filename=self.filename)
            print(f"Added {key} to project metadata under ['data'] and log updated")
        
        def add_sample_data_entry(self, key:str, entry):
            self.sample_data = load(self.filename)["sample_data"]
            self.sample_data[key] = entry
            update(yamlData=self.sample_data, key="sample_data", filename=self.filename)
            print(f"Added {key} to project metadata under ['sample_data'] and log updated")
        
        def add_model_entry(self, key:str, entry):
            self.model = load(self.filename)["model"]
            self.model[key] = entry
            update(yamlData=self.model, key="model", filename=self.filename)
            print(f"Added {key} to project metadata under ['model'] and log updated")

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
            update(yamlData=expCtx, key="context", filename=self.filename)


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

    class ModelCard:
        def __init__(self, model_info:dict={}):
            # if model log file exists, load the metadata
            if model_info:
                self.model_info = model_info
                print("Model info is created with the provided dictionary.")
            else:
                self.model_info = load(faidlog.files["model_yml_file"])["model_info"]
                print("Model info is loaded from the model log file.")

        def get_model_info(self):
            """
            Returns the entire model information.
            """
            return self.model_info

        def set_model_info(self, new_info):
            """
            Sets the model information with new info.
            """
            self.model_info = new_info

        def get_model_detail(self, detail_key):
            """
            Returns a specific detail from the model details.
            """
            return self.model_info.get("model_details", {}).get(detail_key, None)

        def set_model_detail(self, detail_key, detail_value):
            """
            Sets a specific detail in the model details.
            """
            if "model_details" not in self.model_info:
                self.model_info["model_details"] = {}
            self.model_info["model_details"][detail_key] = detail_value

        def get_model_parameter(self, parameter_key):
            """
            Returns a specific parameter from the model parameters.
            """
            return self.model_info.get("model_parameters", {}).get(parameter_key, None)

        def set_model_parameter(self, parameter_key, parameter_value):
            """
            Sets a specific parameter in the model parameters.
            """
            if "model_parameters" not in self.model_info:
                self.model_info["model_parameters"] = {}
            self.model_info["model_parameters"][parameter_key] = parameter_value

        def get_quantitative_analysis(self, metric_key):
            """
            Returns a specific metric from the quantitative analysis.
            """
            metrics = self.model_info.get("quantitative_analysis", {}).get("performance_metrics", [])
            for metric in metrics:
                if metric.get("type") == metric_key:
                    return metric
            return None

        def add_quantitative_metric(self, metric):
            """
            Adds a new metric to the quantitative analysis.
            """
            if "quantitative_analysis" not in self.model_info:
                self.model_info["quantitative_analysis"] = {"performance_metrics": []}
            self.model_info["quantitative_analysis"]["performance_metrics"].append(metric)

        def get_consideration(self, consideration_key):
            """
            Returns a specific consideration from the considerations section.
            """
            considerations = self.model_info.get("considerations", {}).get(consideration_key, [])
            return considerations

        def add_consideration(self, consideration_key, consideration):
            """
            Adds a new consideration to the considerations section.
            """
            if "considerations" not in self.model_info:
                self.model_info["considerations"] = {}
            if consideration_key not in self.model_info["considerations"]:
                self.model_info["considerations"][consideration_key] = []
            self.model_info["considerations"][consideration_key].append(consideration)

        def save(self):
            """
            Saves the model information to the model log file.
            """
            update(self.model_info, key=faidlog.keys["model_info_key"], filename=faidlog.files["model_yml_file"])
            print("Model info saved to the model log file.")
        
        def to_dict(self):
            """
            Returns the model information as a dictionary.
            """
            return self.model_info
        

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
            update(self.to_dict(), key=faidlog.keys["sample_data_key"], filename=faidlog.files["data_yml_file"])
            print("Data info saved to the data log file.")

        def validate(self, schema):
            """
            Validates the data information against a schema.
            """
            from jsonschema import validate
            validate(instance=self.to_dict(), schema=schema)





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
