import os
import inquirer
import click

def load_data(data_path):
    """
    Load data from the specified path
    """
    import pandas as pd
    try:
        data = pd.read_csv(data_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
def get_feature_names(data):
    """
    Get the feature names from the data
    """
    return data.columns.tolist()

def get_data_path():
    """
    List all the files in the specified data folder and return the path of the file selected by the user
    """
    if not os.path.exists('data'):
        print("No data folder found")
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
@click.option('--mod', help='Available options are: init, scan \n init: Initialize the metadata files \n scan: Scan the data for sensitive features.')
@click.option('--data_path', help='Path to the data file')
def main(mod, data_path):
    import sys
    sys.path.append('../..')
    from faid import logging as faidlog
    
    if mod == 'init':
        # Get the main folder name from os
        faidlog.init()
        return
    
    if mod == 'scan-data':
        print("Scanning for sensitive features in the data.")
        # Load data
        if not data_path:
            data_path = get_data_path()
        data = load_data(data_path)
        selected_sensitive_fts = get_sensitive_features(data)
        while not selected_sensitive_fts:
            print("No sensitive features selected. Please select at least one sensitive feature.")
            selected_sensitive_fts = get_sensitive_features(data)
        
        faidlog.add_data_entry("sensitivity_types", selected_sensitive_fts)
        print(selected_sensitive_fts)
   
if __name__ == "__main__":
    main()
