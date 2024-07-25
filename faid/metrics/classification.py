# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from fairlearn.metrics import false_positive_rate
from fairlearn.metrics import false_negative_rate
from fairlearn.metrics import count
from fairlearn.metrics import selection_rate
from fairlearn.metrics import MetricFrame
from sklearn.preprocessing import LabelEncoder

# %%
def tabular_classification(data:pd.DataFrame, sens_feats:list, clf:object):
    """
    Function to calculate fairness metrics for tabular data

    Parameters
    ----------
    data: pd.DataFrame
        Dataframe containing the data
    sens_feats: list
        List of sensitive features
    clf: sklearn classifier model
        ML model object - Default is RandomForestClassifier

    Returns
    -------
    dict
        Dictionary containing the fairness metrics
    """
   # Process data through regular ML Model
    num_feats = data.select_dtypes(include=['int64', 'float64']).columns
    cat_feats = data.select_dtypes(include=['object']).columns

    num_df = data[num_feats]
    cat_df = data[cat_feats]

    # Label encoding
    le = LabelEncoder()
    for i in cat_df:
        cat_df[i] = le.fit_transform(cat_df[i])
    main_df = pd.concat([num_df, cat_df], axis=1)

    X = main_df.drop(main_df.columns[-1], axis=1)
    y = main_df[main_df.columns[-1]]
    # Train/Test splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    # Model Training
    
    if not clf:
        clf = RandomForestClassifier()

    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    
    metrics = {
        "accuracy": accuracy_score,
        "precision":precision_score,
        "false positive rate": false_positive_rate,
        "false negative rate": false_negative_rate,
        "selection rate": selection_rate,
        "count": count,
    }

    metric_frame = MetricFrame(
        metrics = metrics,
        y_true = y_test,
        y_pred = predictions,
        sensitive_features = X_test[sens_feats]
    )
    
    config = {
        "accuracy" : metric_frame.by_group['accuracy'],
        "precision" : metric_frame.by_group['precision'],
        "false positive rate" : metric_frame.by_group['false positive rate'],
        "false negative rate" : metric_frame.by_group['false negative rate'],
        "selection rate" : metric_frame.by_group['selection rate'],
    }

    return config

# %% Example usage
"""
import pandas as pd
data = pd.read_csv('../../../data/german_credit_data.csv')
data.head()
"""