from os import path, makedirs
from faid.logging import initialize_model_log, initialize_exp_log, initialize_data_log, initialize_risk_log, initialize_transparency_log
from faid.logging import get_project_log_path

def init_log():
    if not path.exists(get_project_log_path()):
        makedirs(get_project_log_path())
    initialize_model_log()
    initialize_data_log()
    initialize_risk_log()
    initialize_transparency_log()
