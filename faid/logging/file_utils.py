import os

default_metadata_file_name = "project"
slash = '\\' if os.name == "nt" else "/"

def get_default_metadata_file_name():
  """
  Get the default metadata file
  """
  return default_metadata_file_name


def get_default_metadata_file_name_with_ext():
  """
  Get the default metadata file
  """
  return default_metadata_file_name + ".yml"
# %%
def get_project_log_folder():
    """
    Get the name of the project
    """
    root = os.getcwd()
    log_folder = root + slash + "log"
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    return log_folder + slash