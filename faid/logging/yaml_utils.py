# %%

import os
import yaml
from yaml.parser import ParserError
from .message import error_msg, warning_msg

slash = '\\' if os.name == "nt" else "/"

# %% 
def get_project_log_path():
    """
    Get the name of the project
    """
    root = os.getcwd()
    log_folder = root + slash + "logs" + slash + "faid"
    return log_folder + slash

# %%
def generate(dataDict, filename:str=None, return_result=False):
  """
  Generate a yaml file 
  """
  if not filename:
    print("No file path provided. Please define a file path.")
    return

  if not os.path.exists(get_project_log_path()):
    os.makedirs(get_project_log_path())
  
  if not filename.endswith(".yml"):
    filename = os.path.join(get_project_log_path, f"{filename}.yml")
  
  # The implementation is based on https://github.com/Anthonyhawkins/yamlmaker/
  yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

  def multi_str(dumper, data):
    if '\n' in data:
      return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)
  yaml.add_representer(str, multi_str, Dumper=yaml.SafeDumper)

  if return_result:
    return yaml.safe_dump(dataDict, sort_keys=False, default_flow_style=False)

  with open(filename, 'w') as file:
    yaml.safe_dump(dataDict, file, sort_keys=False, default_flow_style=False)

# %%
def update(yamlData, key:str=None, filename:str=None):
  """
  Update a yaml file
  """
  if not filename.endswith(".yml"):
    filename = os.path.join(get_project_log_path, f"{filename}.yml")
  
  if not os.path.exists(filename):
    warning_msg(f"File {filename} not found. Creating a new file.")
    yamlData = {key: yamlData}
    generate(yamlData, filename)
    return
  
  existing_dataDict = load(filename)

  if existing_dataDict is None:
    existing_dataDict = {}
  
  if key is None:
    generate(yamlData, filename)
    return

  try:
    existing_dataDict[key] = yamlData
  except KeyError:
    print(f"Key {key} not found in the yaml file")
    existing_dataDict.update({key: yamlData})
  
  try:
    generate(existing_dataDict, filename)
  except Exception as e:
    error_msg(f"Error updating yaml file: {e}")

# %%
def load(filename:str):
  """
  Load a yaml file
  """
  import os
  # if filename does not contain .yml extension, add it
  if not filename.endswith(".yml"):
    filename = os.path.join(get_project_log_path(), f"{filename}.yml")

  try:
    with open(filename, 'r') as file:
      return yaml.safe_load(file)
  except FileNotFoundError:
    error_msg(f"File {filename} not found")
  except ParserError:
    error_msg(f"File {filename} is not a valid yaml file")
  
  return {}
