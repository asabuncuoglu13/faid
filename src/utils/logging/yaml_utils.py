# %%

import os
import yaml
from yaml.parser import ParserError
from file_utils import get_project_log_folder, get_default_metadata_file_name
from message import error_msg

# %%
def generate(dataDict, name=None, return_result=False):
  """
  Generate a yaml file 
  """
  if not name:
    filename = get_default_metadata_file_name()
  else:
    filename = name

  filepath = get_project_log_folder() + filename + ".yml"

  # The implementation is based on https://github.com/Anthonyhawkins/yamlmaker/
  yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

  def multi_str(dumper, data):
    if '\n' in data:
      return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)
  yaml.add_representer(str, multi_str, Dumper=yaml.SafeDumper)

  if return_result:
    return yaml.safe_dump(dataDict, sort_keys=False, default_flow_style=False)

  with open(filepath, 'w') as file:
    yaml.safe_dump(dataDict, file, sort_keys=False, default_flow_style=False)

# %%
def update(dataDict, key=None, filename=None):
  """
  Update a yaml file
  """
  if not filename:
    filename = get_default_metadata_file_name()
  filepath = get_project_log_folder() + filename + ".yml"
  if not os.path.exists(filepath):
    error_msg(f"File {filepath} not found")
  existing_dataDict = load()
  # check if key exists
  if key not in existing_dataDict:
    existing_dataDict[key] = dataDict
  else:
    tmpDict = existing_dataDict[key]
    for k, v in dataDict.items():
      tmpDict[k] = v
    existing_dataDict[key] = tmpDict
  generate(existing_dataDict)

# %%
def load(name=None):
  """
  Load a yaml file
  """
  if not name:
    filename = get_project_log_folder() + get_default_metadata_file_name()
  else:
    filename = get_project_log_folder() + name

  try:
    with open(filename + ".yml", 'r') as file:
      return yaml.safe_load(file)
  except FileNotFoundError:
    error_msg(f"File {filename}.yml not found")
  except ParserError:
    error_msg(f"File {filename}.yml is not a valid yaml file")

#  %% Test the functions

dataDict = {
    "project": "FAID",
    "version": "02.0",
    "description": "FAID Test Configuration",
}
updateDict = {
    "seed": 42,
    "accuracy": "0.8"
}

config = {
    "learning_rate": 0.02,
    "architecture": "CNN",
    "dataset": "CIFAR-100",
    "epochs": 10,
}
generate(dataDict)
update(updateDict, key="metrics")
update(config, key="config")
update({"optimizer": "Adam"}, key="config")
print(load()) 

# %%
