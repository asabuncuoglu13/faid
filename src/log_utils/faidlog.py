import os


def get_project_name():
    """
    Get the name of the project
    """
    # Return the full path of the directory
    return os.path.dirname(os.path.realpath(__file__))