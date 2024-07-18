import argparse
import os
import inquirer

from .utils.logging.yaml_utils import update
from .utils.logging.faidlog import init_metadata
from .utils.data.data_utils import load_data, get_feature_names
from .utils.metrics.fairlearn_utils import fairlearn_metrics

def get_data_path():
    """
    Get the path to the data file
    """
    data_path = inquirer.prompt([
        inquirer.Text('input_file',
                      message='Enter the path to the data file:',
                      validate=lambda _, x: os.path.exists(x))
    ])
    return data_path['input_file']

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mod', type = str, help = 'init, scan')
    args = parser.parse_args()

    if args.mod == 'init':
        # Get the main folder name from os
        init_metadata(project_name=os.path.basename(os.getcwd()))
        return
    
    if args.mod == 'scan':
        print("Scanning for sensitive features")
        # Load data
        data_path = get_data_path()
        data = load_data(data_path)
        selected_sensitive_fts = get_sensitive_features(data)
        update(selected_sensitive_fts, key="sensitive_features")
        print(selected_sensitive_fts)
        fairness_score = fairlearn_metrics(data, selected_sensitive_fts)
        update(fairness_score, key="fairness_score")
   
if __name__ == "__main__":
    main()
