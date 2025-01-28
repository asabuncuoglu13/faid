## Log Protected Characteristics

The `log-protected-characteristics.py` script is an example CLI script to showcase scanning a dataset for protected characteristics as defined by the UK Equality Act 2010 and saving it to metadata logs using FAID. The script allows users to select sensitive features from the dataset and logs these features for further analysis.

### Functions

- **load_data(data_path)**: Loads data from the specified CSV file path using pandas.
- **get_feature_names(data)**: Retrieves the feature names (column names) from the loaded dataset.
- **get_data_path()**: Lists all files in the `data` folder and prompts the user to select one.
- **get_protected_characteristics(data)**: Prompts the user to select protected characteristics from the dataset's features using checkboxes.

### Command Line Interface

The script uses the `click` library to provide a command-line interface with the following options:

- **--mod**: Specifies the mode of operation. Available options are:
  - `init`: Initialize the metadata files.
  - `scan`: Scan the data for protected characteristics features.
- **--data_path**: Specifies the path to the data file.

### Usage

To run the script, use the following command:

```sh
python log-protected-characteristics.py --mod scan-data --data_path path/to/your/data.csv
```

If the --data_path is not provided, the script will prompt the user to select a data file from the data folder.

Example
```sh
python log-protected-characteristics.py --mod scan-data --data_path ../credit-scoring-german/data/german_credit_data.csv
```

This command scans the specified data file for protected characteristics and logs the selected features.