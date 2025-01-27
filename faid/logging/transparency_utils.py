from os.path import join, exists
from json import dumps
import re
from collections import defaultdict
from shutil import copy

from faid.logging import error_msg, warning_msg, success_msg, update, load, get_project_log_path, get_current_folder_path

transparency_file_path = join(get_project_log_path(), "transparency.yml")
transparency_file_template_path = join(get_current_folder_path(), "templates/transparency.yml")

def initialize_transparency_log():
    if not exists(transparency_file_path):
        copy(transparency_file_template_path, transparency_file_path)
        success_msg("Transparency log file created.")
    else:
        warning_msg("Transparency log file already exists. Logging will be appended to the existing file.")

def get_transparency_log_path():
    return transparency_file_path

def add_transparency_entry(params:dict, key:str="transparency_info"):
    update(params, key=key, filename=transparency_file_path)
    print(f"Added {key} to transparency metadata")

def get_transparency_entry(key:str=None):
    if key is None:
        return load(transparency_file_path)
    else:
        try:
            return load(transparency_file_path)[key]
        except KeyError:
            error_msg(f"Key {key} not found in the metadata file")
            return None