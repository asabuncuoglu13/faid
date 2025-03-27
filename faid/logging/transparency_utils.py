from os.path import join, exists
from shutil import copy

from faid.logging import error_msg, warning_msg, success_msg, load, get_project_log_path, get_current_folder_path, update

transparency_file_path = join(get_project_log_path(), "transparency.yml")
transparency_file_template_path = join(get_current_folder_path(), "template_example_descriptions/transparency_template_description.yml")

def initialize_transparency_log(test:bool=False):
    if not exists(transparency_file_path):
        if test:
            copy(transparency_file_template_path, transparency_file_path)
            success_msg("Transparency log file created with sample descriptions.")
        else:
            copy(transparency_file_template_path, transparency_file_path)
            success_msg("Transparency log file created.")
    else:
        warning_msg("Transparency log file already exists. Logging will be appended to the existing file.")

def get_transparency_log_path():
    return transparency_file_path

def get_transparency_record():
    try:
        return load(transparency_file_path)
    except FileNotFoundError:
        error_msg("Transparency log file not found. Please create a transparency log file first.")
        return None

def add_transparency_entry(key, entry):
    update(entry, key, filename=transparency_file_path)
    print(f"Added the transparency entry: {entry}.")