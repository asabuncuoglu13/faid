# %%
from jinja2 import Environment, FileSystemLoader
from faid.report import get_faid_report_folder
from faid.logging import (
    load, 
    get_data_entry, 
    get_fairness_log_path,
    get_data_log_path,
    get_model_log_file_path,
    get_risk_register_log_path,
    get_transparency_log_path
)
import os

def generate_all_reports():
    """
    Generate all the reports
    """
    generate_experiment_overview_report()
    generate_model_card_report()
    generate_data_card_report()
    generate_risk_register_report()
    print("All reports generated")

def generate_experiment_overview_report(project_info:dict=None):
    """
    Generate the project overview report
    """
    # for each file starts with fairness_, generate the report
    if project_info is None:
        fairness_files = get_fairness_log_path()
        if isinstance(fairness_files, list):
            for file in fairness_files:
                project_info = load(file)
                experiment_overview_report(project_info)
        else:
            project_info = load(fairness_files)
            experiment_overview_report(project_info)
    else:
        experiment_overview_report(project_info)

def experiment_overview_report(info:dict, output_file:str=None):
    """
    Generates an HTML report from experiment information using Jinja2 template.

    Parameters:
    - experiment_info: Dictionary containing experiment information.
    - output_file: Path to the output HTML file.
    """
    from datetime import datetime

    sample_data_html = None
    # if info has data and data has sample_data
    if "data" in info and "sample_data" in info["data"]:
        import pandas as pd
        sample_data = pd.DataFrame()
        sample_data  = pd.DataFrame(info["data"]["sample_data"])
        sample_data_html = sample_data.to_html()

    captum_records = None
    if "model" in info and "captum_records" in info["model"]:
        from captum.attr import visualization as viz
        import torch
        record = info["model"]["captum_records"]
        visrecord = viz.VisualizationDataRecord(
            torch.tensor(record["word_attributions"], dtype=torch.float64), 
            record["pred_prob"], 
            record["pred_class"],
            record["true_class"], 
            record["attr_class"], 
            record["attr_score"], 
            record["raw_input_ids"], 
            record["convergence_score"])
        captum_records = viz.visualize_text([visrecord])._repr_html_()
    
    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/experiment_overview_template.html')
    # Render the template with metrics
    html_content = template.render(info, sample_data=sample_data_html, captum_records = captum_records)

    if output_file is None:
        if "name" not in info:
            name = datetime.now().isoformat()
        else:
            name = info["name"]
        output_file = f"experiment_overview_{name}.html"
    
    output_file = get_faid_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

def generate_risk_register_report(custom_file_path:str=None):
    """
    Generate the risk register report
    """
    import os
    if not os.path.exists(get_risk_register_log_path()):
        print("Risk log file not found")
        return
    else:
        if custom_file_path is None:
            raid_register_report()
        else:
            if os.path.exists(custom_file_path):
                info = load(custom_file_path)
                raid_register_report(risk_data=info)
            else:
                print("Custom file path not found")

def raid_register_report(risk_data:dict={}, output_file:str="risk_register.html"):
    """
    Generates an HTML report from risk data in format format using Jinja2 template.

    Parameters:
    - raid_data: Dictionary containing RAID (Risks, Assumptions, Issues, Dependencies) data.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/risk_register_template.html')

    if risk_data == {}:  # Load the data from the yaml file
        try:
            raid_data = load("risks")
        except FileNotFoundError:
            print("RAID data not found. Please provide RAID data in the YAML file.")

    # Render the template with metrics
    html_content = template.render(data = raid_data)

    output_file = get_faid_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

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
        info = get_data_entry()
        if not os.path.exists(get_data_log_path()):
            print("Data log file not found")
            return
        else:
            if output_file_path is not None:
                data_card(dataset_info=info, output_file=output_file_path)
            else:
                data_card(dataset_info=info)

def data_card(dataset_info:dict={}, output_file:str="data_card.html"):
    """
    Generates an HTML report from data card information using Jinja2 template.

    Parameters:
    - dataset_info: Dictionary containing dataset information.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/data_card_template.html')

    if dataset_info == {}:  # Load the data from the yaml file
        try:
            dataset_info = load("data")
        except FileNotFoundError:
            print("Data card information not found. Please provide data card information in the YAML file.")
    # Render the template with metrics
    html_content = template.render(dataset_info)

    output_file = get_faid_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)


def generate_model_card_report(custom_file_path:str=None):
    """
    Generate the model card report
    """
    import os
    if not os.path.exists(get_model_log_file_path()):
        print("Model log file not found")
        return
    else:
        if custom_file_path is None:
            model_card()
        else:
            if os.path.exists(custom_file_path):
                info = load(custom_file_path)
                model_card(model_info=info)
            else:
                print("Custom file path not found")

def model_card(model_info:dict={}, output_file:str="model_card.html"):
    """
    Generates an HTML model card from model info using Jinja2 template.

    Parameters:
    - model_info: Dictionary containing all model information.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/model_card_template.html')

    if model_info == {}:  # Load the data from the yaml file
        try:
            model_info = load("model")
        except FileNotFoundError:
            print("Model card information not found. Please provide model card information in the YAML file.")
    # Render the template with metrics
    html_content = template.render(model_info)

    output_file = get_faid_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

def generate_transparency_report(custom_file_path:str=None):
    """
    Generate the transparency report
    """
    import os
    if not os.path.exists(get_transparency_log_path()):
        print("Transparency log file not found")
        return
    else:
        if custom_file_path is None:
            transparency_report()
        else:
            if os.path.exists(custom_file_path):
                info = load(custom_file_path)
                transparency_report(transparency_data=info)
            else:
                print("Custom file path not found")

def transparency_report(transparency_data:dict={}, output_file:str="transparency.html"):
    """
    Generates an HTML report from transparency data using Jinja2 template.

    Parameters:
    - transparency_data: Dictionary containing transparency information.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/transparency.html')

    if transparency_data == {}:  # Load the data from the yaml file
        try:
            raid_data = load("transparency")
        except FileNotFoundError:
            print("Transparency data not found. Please provide transparency data in the YAML file.")
    # Render the template with metrics
    html_content = template.render(raid_data)

    output_file = get_faid_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)