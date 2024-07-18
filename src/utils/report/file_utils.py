import os
slash = '\\' if os.name == "nt" else "/"

# %%
def get_project_report_folder():
    """
    Get the name of the project
    """
    root = os.getcwd()
    report_folder = root + slash + "reports"
    if not os.path.exists(report_folder):
        os.mkdir(report_folder)
    return report_folder + slash