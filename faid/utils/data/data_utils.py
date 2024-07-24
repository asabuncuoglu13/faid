import pandas as pd

def load_data(file_path):
    """
    Load data from a csv file
    """
    return pd.read_csv(file_path)


def get_feature_names(data):
    """
    Get the feature names from the data
    """
    return data.columns.tolist()