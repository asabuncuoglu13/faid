import os
import datetime
from .yaml_utils import generate, update, load

def init_metadata(project_name, author=None, date=None, description=None, version=None):
    """
    Initialize the metadata
    """
    metadata = {
        "project": project_name,
        "author": author if author else "Author",
        "date": date if date else datetime.date.today().isoformat(),
        "description": description if description else "",
        "version": version if version else "0.1.0"
    }
    generate(metadata)
    return metadata  # Return the metadata dictionary


def update_metadata(dataDict, key=None):
    """
    Update the metadata
    """
    update(dataDict, key=key)

def print():
    """
    Print the metadata
    """
    print(load())