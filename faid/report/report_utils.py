# %%
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from .file_utils import get_project_report_folder
from ..logging.yaml_utils import load
import os

# %%
def generate_project_overview_report(project_info:dict={}, output_file:str="project_overview.html"):
    """
    Generates an HTML report from project information using Jinja2 template.

    Parameters:
    - project_info: Dictionary containing project information.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/project_overview_template.html')

    if project_info == {}:  # Load the data from the yaml file
        project_info = load("project")
        print(project_info)
    # Render the template with metrics
    html_content = template.render(project_info)

    output_file = get_project_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)
# %%
def generate_fairness_report(sample_data:pd.DataFrame=pd.DataFrame(), 
                             metrics: dict=None, 
                             group_metrics: dict=None,
                             output_file:str="fairness_report.html"):
    """
    Generates an HTML report from fairness metrics using Jinja2 template.

    Parameters:
    - metrics: Dictionary containing overall model metrics.
    - group_metrics: Dictionary containing fairness metrics by group.
    - output_file: Path to the output HTML file.
    """
    
    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/fairness_template.html')

    # Render the template with metrics
    if sample_data.empty:
        sample_data = load("fairness")
        sample_data  = pd.DataFrame(sample_data["sample_results"])
        print(sample_data)

    html_content = template.render(sample_data=sample_data.to_html(), metrics=metrics, group_metrics=group_metrics)

    output_file = get_project_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

# %%
def generate_raid_register_report(raid_data:dict={}, output_file:str="risk_register.html"):
    """
    Generates an HTML report from risk data in format format using Jinja2 template.

    Parameters:
    - raid_data: Dictionary containing RAID (Risks, Assumptions, Issues, Dependencies) data.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/risk_register.html')

    if raid_data == {}:  # Load the data from the yaml file
        raid_data = load("risks")
        print(raid_data)
    # Render the template with metrics
    html_content = template.render(raid_data)

    output_file = get_project_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

# %%
def generate_data_card(dataset_info:dict={}, output_file:str="data_card.html"):
    """
    Generates an HTML report from data card information using Jinja2 template.

    Parameters:
    - dataset_info: Dictionary containing dataset information.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/data_card_template.html')

    if dataset_info == {}:  # Load the data from the yaml file
        dataset_info = load("data")
        print(dataset_info)
    # Render the template with metrics
    html_content = template.render(dataset_info)

    output_file = get_project_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)


# %%
def generate_model_card(model_info:dict={}, output_file:str="model_card.html"):
    """
    Generates an HTML model card from model info using Jinja2 template.

    Parameters:
    - model_info: Dictionary containing all model information.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/model_card_template.html')

    if model_info == {}:  # Load the data from the yaml file
        model_info = load("model")
        print(model_info)
    # Render the template with metrics
    html_content = template.render(model_info)

    output_file = get_project_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

# %%
def generate_transparency_report(transparency_data:dict={}, output_file:str="transparency.html"):
    """
    Generates an HTML report from transparency data using Jinja2 template.

    Parameters:
    - transparency_data: Dictionary containing transparency information.
    - output_file: Path to the output HTML file.
    """

    # Load Jinja2 template
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_folder_location))
    template = env.get_template('templates/transparency.html')

    if transparency_data == {}:  # Load the data from the yaml file
        raid_data = load("transparency")
        print(raid_data)
    # Render the template with metrics
    html_content = template.render(raid_data)

    output_file = get_project_report_folder() + output_file
    # Write the rendered HTML to a file
    with open(output_file, 'w') as file:
        file.write(html_content)

# %% Example usa of generation methods
"""
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

generate_fairness_report(metrics=overall_metrics, group_metrics=group_metrics, 'fairness_report.html')
"""

"""
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
"""

"""
dataset_info = {
	"dataset_name": "Financial Sentiment Analysis Dataset",
	"summary": "A dataset for sentiment analysis in the financial domain, including news articles and analyst reports.",
	"dataset_link": "http://example.com/financial-sentiment-dataset",
	"authors": [
		{"name": "Alex Johnson", "team": "Financial Analytics", "role": "Data Scientist"},
		{"name": "Samantha Green", "team": "Data Engineering", "role": "Data Engineer"}
	],
	"publishing_organization": "Financial Insights Inc.",
	"industry_types": ["Finance", "Data Analytics"],
	"publishing_poc": {
		"name": "Michael Brown",
		"affiliation": "Financial Insights Inc.",
		"contact": "michael.brown@example.com",
		"mailing_list": "finance-data-updates@example.com",
		"website": "http://financialinsights.com"
	},
	"dataset_owners": {
		"team": "Financial Data Team",
		"name": "Financial Data Team",
		"affiliation": "Financial Insights Inc.",
		"contact": "data-team@example.com",
		"group_email": "data-team@example.com",
		"website": "http://financialinsights.com/data-team"
	},
	"dataset_authors": [
		{"name": "Alex Johnson", "title": "Data Scientist", "affiliation": "Financial Insights Inc.", "year": "2023"}
	],
	"funding_sources": ["Finance Research Grants", "Investor Funding"],
	"data_subjects": ["Market Sentiment", "Investment Trends", "Economic Indicators"],
	"dataset_snapshot": {
		"Total Records": "500,000",
		"Coverage": "Global Financial Markets",
		"Time Span": "2015-2023"
	},
	"content_description": "This dataset includes sentiment-labeled financial news articles and analyst reports, designed for training and evaluating sentiment analysis models.",
	"descriptive_statistics": {
		"fields": ["Positive", "Neutral", "Negative"],
		"stats": [
			{"name": "News Articles", "values": ["40%", "30%", "30%"]},
			{"name": "Analyst Reports", "values": ["50%", "20%", "30%"]}
		]
	},
	"sensitivity_types": ["Confidential Information"],
	"intentional_sensitive_data": [
		{"name": "Financial Reports", "description": "Analyst reports and financial statements."}
	],
	"unintentional_sensitive_data": [],
	"security_privacy_handling": "All data is anonymized and confidential information is removed to ensure privacy.",
	"risk_types": ["Data Misuse", "Financial Misinterpretation"],
	"risks_mitigations": "Data usage guidelines and strict access controls are implemented to mitigate risks.",
	"maintenance_status": "Actively Maintained",
	"version_details": {
		"current_version": "2.0",
		"last_updated": "2023-01-01",
		"release_date": "2022-05-01"
	},
	"maintenance_plan": "Biannual updates with new data and model refinements.",
	"next_update": {
		"version_affected": "2.1",
		"next_data_update": "2023-11-01",
		"next_version": "2.1",
		"next_version_update": "2023-11-01"
	},
	"expected_changes": "Expansion of dataset to include more global financial markets and updated sentiment analysis.",
	"primary_data_modality": "Text",
	"sampling_data_points": [
		{"url": "http://example.com/sample-article-1", "name": "Sample Article 1"},
		{"url": "http://example.com/sample-report-1", "name": "Sample Report 1"}
	],
	"data_fields": [
		{"name": "Article Text", "value": "Text", "description": "The body text of the news article."},
		{"name": "Sentiment", "value": "Label", "description": "Sentiment label (Positive, Neutral, Negative)."}
	],
	"typical_data_point": "A record includes the text of a financial news article or analyst report along with its sentiment label."
}

generate_data_card(dataset_info, 'data_card.html')
"""

"""
model_info = {
    "schema_version": "0.0.1",
    "model_details": {
        "name": "Example Model Name",
        "overview": "This is a brief one-line description of the model.",
        "documentation": "Here is a thorough description of the model, including its purpose and usage.",
        "owners": [
            {
                "name": "Owner Name",
                "contact": "owner@example.com"
            }
        ],
        "version": {
            "name": "1.0",
            "date": "2023-01-01",
            "diff": "Initial version."
        },
        "licenses": [
            {
                "identifier": "MIT",
                "custom_text": ""
            }
        ],
        "references": [
            {
                "reference": "http://example.com/model-reference"
            }
        ],
        "citations": [
            {
                "style": "APA",
                "citation": "Author, A. (Year). Title of document. Publisher."
            }
        ],
        "path": "/path/to/model"
    },
    "model_parameters": {
        "model_architecture": "CNN",
        "data": [
            {
                "name": "Dataset Name",
                "link": "http://example.com/dataset",
                "sensitive": {
                    "sensitive_data": ["Personal Information"]
                },
                "graphics": {
                    "description": "Sample images from the dataset",
                    "collection": [
                        {
                            "name": "Sample Image",
                            "image": "base64EncodedString"
                        }
                    ]
                },
                "description": "This dataset includes..."
            }
        ],
        "input_format": "JPEG",
        "input_format_map": [
            {
                "key": "image",
                "value": "JPEG"
            }
        ],
        "output_format": "Probability",
        "output_format_map": [
            {
                "key": "label",
                "value": "Probability"
            }
        ]
    },
    "quantitative_analysis": {
        "performance_metrics": [
            {
                "type": "Accuracy",
                "value": "95%",
                "slice": "Validation Set",
                "confidence_interval": {
                    "lower_bound": "94%",
                    "upper_bound": "96%"
                }
            }
        ],
        "graphics": {
            "description": "Performance metrics graphs",
            "collection": [
                {
                    "name": "Accuracy Over Time",
                    "image": "base64EncodedString"
                }
            ]
        }
    },
    "considerations": {
        "users": [
            {
                "description": "Data scientists and ML engineers"
            }
        ],
        "use_cases": [
            {
                "description": "Image classification for identifying objects."
            }
        ],
        "limitations": [
            {
                "description": "Struggles with low-light images."
            }
        ],
        "tradeoffs": [
            {
                "description": "Higher accuracy for increased computational cost."
            }
        ],
        "ethical_considerations": [
            {
                "name": "Bias in Training Data",
                "mitigation_strategy": "Use a diverse dataset."
            }
        ]
    }
}
generate_model_card(model_info, 'data_card.html')
"""
# %%
