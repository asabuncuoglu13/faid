# %%
from jinja2 import Environment, FileSystemLoader
from file_utils import get_project_report_folder

# %%
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
    template = env.get_template('templates/fairness_metrics.html')

    # Render the template with metrics
    html_content = template.render(metrics=metrics, group_metrics=group_metrics)

    output_file = get_project_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

# %%
def generate_raid_register_report(raid_data, output_file):
    """
    Generates an HTML report from fairness metrics using Jinja2 template.

    Parameters:
    - metrics: Dictionary containing overall model metrics.
    - group_metrics: Dictionary containing fairness metrics by group.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/risk_register.html')

    # Render the template with metrics
    html_content = template.render(raid_data)

    output_file = get_project_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)


# %% Example usa of generate_fairness_report

overall_metrics = {
    'Accuracy': 0.85,
    'Precision': 0.82,
    'Recall': 0.88
}

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

generate_fairness_report(overall_metrics, group_metrics, 'fairness_report.html')
# %% Example usa of generate_raid_register_report
raid_data = {
    'risks': [
        {
            'id': 'R1',
            'description': "Risk of biased AI model outputs due to unrepresentative training data.",
            'impact': "High",
            'likelihood': "High",
            'mitigation': "Ensure diverse and representative training data; implement bias detection mechanisms."
        },
        {
            'id': 'R2',
            'description': "Risk of non-compliance with AI fairness regulations.",
            'impact': "High",
            'likelihood': "Medium",
            'mitigation': "Stay updated with regulations and ensure compliance throughout the development process."
        }
    ],
    'assumptions': [
        {
            'id': 'A1',
            'description': "Assume that the training data provided is accurate and reliable.",
            'impact': "High",
            'action': "Perform data validation and quality checks."
        }
    ],
    'issues': [
        {
            'id': 'I1',
            'description': "Detected bias in initial AI model outputs.",
            'impact': "High",
            'status': "Open",
            'action': "Investigate the source of bias and retrain the model with improved data."
        }
    ],
    'dependencies': [
        {
            'id': 'D1',
            'description': "Dependency on external datasets for training the AI model.",
            'impact': "High",
            'status': "Pending",
            'action': "Ensure timely access to required datasets from data providers."
        }
    ]
}
generate_raid_register_report(raid_data, 'raid_register.html')
# %%
