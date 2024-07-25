import os
import inquirer
import click

from .utils.logging.yaml_utils import update
from .faidlog import init_metadata
from .utils.logging.message import error_msg, warning_msg, info_msg
from .utils.data.data_utils import load_data, get_feature_names
from .metrics.classification import tabular_classification

def get_data_path():
    """
    List all the files in the specified data folder and return the path of the file selected by the user
    """
    if not os.path.exists('data'):
        warning_msg("No data folder found")
        return
    
    data_filename = inquirer.prompt([
        inquirer.List('input_file',
                    message='Select the data file',
                    choices=os.listdir('data'),
                    carousel=True)
    ])

    return os.path.join('data', data_filename['input_file'])

def get_sensitive_features(data):
    """
    Get the sensitive features from the data with user input
    """
    # Get feature names
    feature_list = get_feature_names(data)
    # Prompt the user to select features using checkboxes
    sensitive_fts = inquirer.prompt([
        inquirer.Checkbox('features',
                        message='Use your spacebar to select sensitive features:',
                        choices=feature_list,
                        carousel=True)
    ])

    selected_sensitive_fts = sensitive_fts['features']
    return selected_sensitive_fts

@click.command()
@click.option('--mod', help='Available options are: init, scan \n init: Initialize the metadata file \n scan: Scan the data for sensitive features.')
@click.option('--data_path', help='Path to the data file')
def main(mod, data_path):
    if mod == 'init':
        # Get the main folder name from os
        init_metadata(project_name=os.path.basename(os.getcwd()))
        return
    
    if mod == 'scan-data':
        info_msg("Scanning for sensitive features in the data.")
        # Load data
        if not data_path:
            data_path = get_data_path()
        data = load_data(data_path)
        selected_sensitive_fts = get_sensitive_features(data)
        while not selected_sensitive_fts:
            warning_msg("No sensitive features selected. Please select at least one sensitive feature.")
            selected_sensitive_fts = get_sensitive_features(data)
        update(selected_sensitive_fts, key="sensitive_features")
        print(selected_sensitive_fts)
        #fairness_score = tabular_classification(data, selected_sensitive_fts)
        #update(fairness_score, key="fairness_score")
   
if __name__ == "__main__":
    main()
