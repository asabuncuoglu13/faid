import numpy as np
from sklearn.metrics import (
    brier_score_loss,
    log_loss,
    accuracy_score,
    f1_score,
    average_precision_score,
)
from sklearn.calibration import calibration_curve
from fairlearn.metrics import make_derived_metric

def true_positive_score(y_true, y_pred):
    return (y_true & y_pred).sum() / y_true.sum()

def false_positive_score(y_true, y_pred):
    return (1 - y_true & y_pred).sum() / (1 - y_true).sum()

def false_negative_score(y_true, y_pred):
    return 1 - true_positive_score(y_true, y_pred)

def average_log_loss_score(y_true, y_pred):
    """Average log loss function."""
    return np.mean(log_loss(y_true, y_pred))

def miscalibration_score(y_true, y_pred, n_bins=10):
    """Miscalibration score. Calibration is the difference between the predicted and the true probability of the positive class."""
    prob_true, prob_pred = calibration_curve(y_true, y_pred, n_bins=n_bins)
    return np.mean(np.abs(prob_true - prob_pred))

def brier_score_loss_diff(y_true, y_pred, sensitive_features):
    brier = make_derived_metric(metric=brier_score_loss, transform="difference")
    return brier(y_true, y_pred, sensitive_features)

def brier_score_loss_ratio(y_true, y_pred, sensitive_features):
    brierl = make_derived_metric(metric=brier_score_loss, transform="ratio")
    return brierl(y_true, y_pred, sensitive_features)

def log_loss_diff(y_true, y_pred, sensitive_features):
    log = make_derived_metric(metric=log_loss, transform="difference")
    return log(y_true, y_pred, sensitive_features)

def log_loss_ratio(y_true, y_pred, sensitive_features):
    logl = make_derived_metric(metric=log_loss, transform="ratio")
    return logl(y_true, y_pred, sensitive_features)

def accuracy_diff(y_true, y_pred, sensitive_features):
    accs = make_derived_metric(metric=accuracy_score, transform="difference")
    return accs(y_true, y_pred, sensitive_features)

def accuracy_ratio(y_true, y_pred, sensitive_features):
    accr = make_derived_metric(metric=accuracy_score, transform="ratio")
    return accr(y_true, y_pred, sensitive_features)

def f1_diff(y_true, y_pred, sensitive_features):
    f1s = make_derived_metric(metric=f1_score, transform="difference")
    return f1s(y_true, y_pred, sensitive_features)

def f1_ratio(y_true, y_pred, sensitive_features):
    f1r = make_derived_metric(metric=f1_score, transform="ratio")
    return f1r(y_true, y_pred, sensitive_features)

def avg_precision_diff(y_true, y_pred, sensitive_features):
    auprc = make_derived_metric(metric=average_precision_score, transform="difference")
    return auprc(y_true, y_pred, sensitive_features)

def avg_precision_ratio(y_true, y_pred, sensitive_features):
    auprcr = make_derived_metric(metric=average_precision_score, transform="ratio")
    return auprcr(y_true, y_pred, sensitive_features)