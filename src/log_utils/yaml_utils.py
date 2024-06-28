# %%

import os
import subprocess
import sys
import yaml
from yaml.parser import ParserError
from faidlog import get_project_name

# The implementation is based on https://github.com/Anthonyhawkins/yamlmaker/

# %%
def error_msg(msg):
  """
  Print an error message and exit
  """
  print(f"Error: {msg}")
  sys.exit(1)

# %%
def generate(config, name=None, return_result=False):
  """
  Generate a yaml file 
  """
  if not name:
    slash = '\\' if os.name == "nt" else "/"
    filename = get_project_name() + slash + "config"
  else:
    filename = name

  yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

  def multi_str(dumper, data):
    if '\n' in data:
      return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)
  yaml.add_representer(str, multi_str, Dumper=yaml.SafeDumper)
  yaml.SafeDumper.ignore_aliases = lambda *args: True

  if return_result:
    return yaml.safe_dump(config, sort_keys=False, default_flow_style=False)

  if os.path.exists(filename + ".yml"):
    existing_config = load(filename)
    existing_config.update(config)
    config = existing_config
  with open(filename + ".yml", 'w') as file:
    yaml.safe_dump(config, file, sort_keys=False, default_flow_style=False)

# %%

def load(name=None):
  """
  Load a yaml file
  """
  if not name:
    slash = '\\' if os.name == "nt" else "/"
    filename = get_project_name() + slash + "config"
  else:
    filename = name

  try:
    with open(filename + ".yml", 'r') as file:
      return yaml.safe_load(file)
  except FileNotFoundError:
    error_msg(f"File {filename}.yml not found")
  except ParserError:
    error_msg(f"File {filename}.yml is not a valid yaml file")

#  %% Test the functions
config = {
    "name": "James",
    "age": 25,
    "city": "New York"
}

generate(config)
print(load())
# %%
