from os.path import join, exists
from shutil import copy
import collections

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
def add_risk_entry(description:str, impact:str, likelihood:str, mitigation:str):
    """
    Add a risk entry to the risk register
    Key can be one of ["risks", "assumptions", "issues", "dependencies"]
    """
    # add an id to the risk entry
    risk_data = load(risk_file_path)["risks"]

    # if the risk_data is empty, set the id to 0
    if len(risk_data) == 0:
        id = 0
    else:
        id = len(risk_data)

    # if the risk data contains an entry with the same description, do not add it
    for risk in risk_data.values():
        if risk["description"] == description:
            error_msg(f"Risk with description {description} already exists.")
            return
    
    update({id: {
        "description": description,
        "impact": impact,
        "likelihood": likelihood,
        "mitigation": mitigation
        }}, key="risks", filename=risk_file_path)
    print(f"Added the risk: {description}.")

@staticmethod
def add_assumption_entry(description: str, impact: str, action: str):
    """
    Add an assumption entry to the risk register
    """
    assumption_data = load(risk_file_path)["assumptions"]

    if len(assumption_data) == 0:
        id = 0
    else:
        id = len(assumption_data)

    for assumption in assumption_data.values():
        if assumption["description"] == description:
            error_msg(f"Assumption with description {description} already exists.")
            return

    update({id: {
        "description": description,
        "impact": impact,
        "action": action
        }}, key="assumptions" ,filename=risk_file_path)
    print(f"Added the assumption: {description}.")

@staticmethod
def add_issue_entry(description: str, impact: str, status: str, action: str):
    """
    Add an issue entry to the risk register
    """
    issue_data = load(risk_file_path)["issues"]

    if len(issue_data) == 0:
        id = 0
    else:
        id = len(issue_data)

    for issue in issue_data.values():
        if issue["description"] == description:
            error_msg(f"Issue with description {description} already exists.")
            return

    update({id: {
        "description": description,
        "impact": impact,
        "status": status,
        "action": action
        }}, key="issues", filename=risk_file_path)
    print(f"Added the issue: {description}.")

@staticmethod
def add_dependency_entry(description: str, impact: str, status: str, action: str):
    """
    Add a dependency entry to the risk register
    """
    dependency_data = load(risk_file_path)["dependencies"]

    if len(dependency_data) == 0:
        id = 0
    else:
        id = len(dependency_data)

    for dependency in dependency_data.values():
        if dependency["description"] == description:
            error_msg(f"Dependency with description {description} already exists.")
            return

    update({id: {
        "description": description,
        "impact": impact,
        "status": status,
        "action": action
    }}, key="dependencies", filename=risk_file_path)
    print(f"Added the dependency: {description}.")

@staticmethod
def get_risk_entries():
    try:
        return load(risk_file_path)["risks"]
    except KeyError:
        error_msg("Risk field could not be found in the metadata file")
        return None
    
@staticmethod
def get_assumption_entries():
    try:
        return load(risk_file_path)["assumptions"]
    except KeyError:
        error_msg("Assumption field could not be found in the metadata file")
        return None

@staticmethod
def get_issue_entries():
    try:
        return load(risk_file_path)["issues"]
    except KeyError:
        error_msg("Issue field could not be found in the metadata file")
        return None
    
@staticmethod
def get_dependency_entries():
    try:
        return load(risk_file_path)["dependencies"]
    except KeyError:
        error_msg("Dependency field could not be found in the metadata file")
        return None