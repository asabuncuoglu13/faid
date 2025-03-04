from os.path import join, exists
from json import dumps
import re
from collections import defaultdict
from shutil import copy

from faid.logging import error_msg, warning_msg, success_msg, update, load, get_project_log_path, get_current_folder_path

risk_file_path = join(get_project_log_path(), "risks.yml")
risk_file_template_path = join(get_current_folder_path(), "templates/risks.yml")
risk_file_template_with_description_path = join(get_current_folder_path(), "template_example_descriptions/risks_template_description.yml")

def initialize_risk_log(test:bool=False):
    if not exists(risk_file_path):
        if test:
            copy(risk_file_template_with_description_path, risk_file_path)
            success_msg("Risks log file created with sample descriptions.")
        else:
            copy(risk_file_template_path, risk_file_path)
            success_msg("Risks log file created.")
    else:
        warning_msg("Risks log file already exists. Logging will be appended to the existing file.")

def get_risk_register_log_path():
    return risk_file_path

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
    risk_data = load(risk_file_path)
    id = len(risk_data[key]) + 1

    update({id: params}, key=key, filename=risk_file_path)
    print(f"Added {key} to risk register")

@staticmethod
def get_risk_entry(key:str=None):
    if key is None:
        return load(risk_file_path)
    else:
        try:
            return load(risk_file_path)[key]
        except KeyError:
            error_msg(f"Key {key} not found in the metadata file")
            return None