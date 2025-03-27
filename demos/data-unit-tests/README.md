# Data Unit Tests

A **data unit test** is a test designed to validate the quality, integrity, and behavior of data at various stages of an ML pipeline. It ensures that datasets, features, and data transformations meet expected standards and assumptions. These tests catch issues like missing values, data drift, or violations of fairness constraints.

**Integrating Data Unit Tests in a CI/CD Pipeline:**

1. **Pre-processing Stage**:
   - Add data unit tests as part of pre-deployment checks.
   - Automatically trigger the tests whenever new datasets, preprocessing scripts, or feature engineering code is updated.
   
2. **Automation**:
   - Use CI/CD tools (e.g., GitHub Actions, Jenkins) to run test suites.
   - Run tests on incoming datasets or simulated pipelines before the ML model is trained.

3. **Examples of Tests**:
   - Check for **missing data** or anomalies (e.g., nulls, outliers).
   - Validate **feature distributions** against historical data to detect drift.
   - Enforce schema validations (e.g., column types, ranges).

**Using Data Unit Tests for ML Fairness Assessments:**

1. **Fairness Metrics**: Include unit tests to monitor fairness metrics, such as:
   - **Demographic Parity**: Ensure predicted outcomes are similar across groups (e.g., gender, race).
   - **Equal Opportunity**: Check true positive rates across sensitive groups.

2. **Bias Detection**:
   - Run tests that compare model outputs across subgroups (e.g., does the model favor one group over another?).
   - Validate against predefined fairness thresholds (e.g., a maximum acceptable disparity).

3. **Data Integrity for Fairness**:
   - Test for **representation bias** (e.g., ensure sensitive groups are adequately represented in training data).
   - Monitor feature correlations with sensitive attributes to avoid leakage.

This notebook demonstrates sample data unit tests as well as using a specialised library (Great Expectations) for this purpose. [NOTE: My personal experience is using this library is an overkill. It is not easy to integrate it into workflows. However, it might be useful for some specific use cases.]

## Create a Script for Metadata Management throughout CI/CD

At some point, you need to create some scripts to include, test, and verify data in a script, so that CI/CD automation can produce the PASS/FAIL results.

The `log-protected-characteristics.py` script is an example CLI script to showcase scanning a dataset for protected characteristics as defined by the UK Equality Act 2010 and saving it to metadata logs using FAID. The script allows users to select sensitive features from the dataset and logs these features for further analysis.

The script also demonstrate using the `click` library in case you have access to a command-line interface interactively.  You can test this library using the following options:

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