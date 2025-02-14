# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from fairlearn.metrics import false_positive_rate
from fairlearn.metrics import false_negative_rate
from fairlearn.metrics import count
from fairlearn.metrics import selection_rate
from fairlearn.metrics import MetricFrame
from sklearn.preprocessing import LabelEncoder

# %%
def tabular_classification(X:pd.DataFrame, y, sens_feats:list, clf:object=RandomForestClassifier()):
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
    num_feats = X.select_dtypes(include=['int64', 'float64']).columns
    cat_feats = X.select_dtypes(include=['object', 'category']).columns

    num_df = X[num_feats]
    cat_df = X[cat_feats]

    # Label encoding
    le = LabelEncoder()
    for i in cat_df:
        cat_df.loc[:, i] = le.fit_transform(cat_df[i])
    main_df = pd.concat([num_df, cat_df], axis=1)

    main_df = main_df.dropna()
    
    X_train, X_test, y_train, y_test = train_test_split(main_df, y, test_size=0.2, random_state=42, stratify=y)
    
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

def benchmark_tabular_classification(X: pd.DataFrame, y, sens_feats: list):
    """
    Function to benchmark fairness metrics with multiple classifiers for tabular data

    Parameters
    ----------
    data: pd.DataFrame
        Dataframe containing the data
    sens_feats: list
        List of sensitive features

    Returns
    -------
    dict
        Dictionary containing the fairness metrics for each classifier
    """
    classifiers = {
        "RandomForest": RandomForestClassifier(),
        "LogisticRegression": LogisticRegression(),
        "DecisionTree": DecisionTreeClassifier(),
        "SVC": SVC()
    }

    results = {}

    for clf_name, clf in classifiers.items():
        metrics = tabular_classification(X, y, sens_feats, clf)
        results[clf_name] = metrics

    return results