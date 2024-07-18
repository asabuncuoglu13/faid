# %%
from jinja2 import Environment, FileSystemLoader
import sys
import os
from file_utils import get_project_report_folder

def generate_fairness_report(metrics: dict, group_metrics: dict, output_file: str):
    """
    Generates an HTML report from fairness metrics using Jinja2 template.

    Parameters:
    - metrics: Dictionary containing overall model metrics.
    - group_metrics: Dictionary containing fairness metrics by group.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')

    # Render the template with metrics
    html_content = template.render(metrics=metrics, group_metrics=group_metrics)

    output_file = get_project_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)


# %% Example usage
"""
overall_metrics = {
    'Accuracy': 0.85,
    'Precision': 0.82,
    'Recall': 0.88
}

# Example group metrics
group_metrics = {
    'Accuracy': {
        'Group A': 0.80,
        'Group B': 0.90
    },
    'Precision': {
        'Group A': 0.78,
        'Group B': 0.85
    },
    'Recall': {
        'Group A': 0.83,
        'Group B': 0.92
    }
}

# Generate the report
generate_fairness_report(overall_metrics, group_metrics, 'fairness_report.html')
"""
# %%
