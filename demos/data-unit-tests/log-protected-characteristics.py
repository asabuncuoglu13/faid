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

def get_protected_characteristics(data):
    """
    Get the sensitive features from the data with user input
    """
    # Get feature names
    feature_list = get_feature_names(data)
    # Prompt the user to select features using checkboxes
    sensitive_fts = inquirer.prompt([
        inquirer.Checkbox('features',
                        message='Use your spacebar to select protected characteristics features. UK Equality Act 2010 defines 9 protected characteristics: Age, Disability, Gender Reassignment, Marriage and civil partnership, Pregnancy and maternity, Race, Religion or belief, Sex, Sexual orientation.',
                        choices=feature_list,
                        carousel=True)
    ])

    selected_protected_fts = sensitive_fts['features']
    return selected_protected_fts

@click.command()
@click.option('--mod', help='Available options are: init, scan \n init: Initialize the metadata files \n scan: Scan the data for protected characteristics features.')
@click.option('--data_path', help='Path to the data file')
def main(mod, data_path):
    import sys
    sys.path.append('../..')
    from faid import logging as faidlog
    
    faidlog.init_log()
    
    if mod == 'scan-data':
        print("Scanning for protected characteristics in the data.")
        # Load data
        if not data_path:
            data_path = get_data_path()
        data = load_data(data_path)
        selected_protected_fts = get_protected_characteristics(data)
        while not selected_protected_fts:
            print("No protected characteristics selected. Please select at least one protected characteristic.")
            selected_protected_fts = get_protected_characteristics(data)
        
        print(selected_protected_fts)
        faidlog.add_data_entry(key="sensitive_data", entry={"protected_characteristics" : selected_protected_fts})
        print(selected_protected_fts)
   
if __name__ == "__main__":
    main()
    # python log-protected-characteristics.py --mod scan-data --data_path ../credit-scoring-german/data/german_credit_data.csv
