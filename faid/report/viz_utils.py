import os
import json
import matplotlib.figure
import plotly.graph_objects as go

import base64
import io
import matplotlib

from faid.logging import (
    load,
    get_fairness_log_path
)

def figure_to_base64str(fig: matplotlib.figure.Figure) -> str:
  """Converts a Matplotlib figure to a base64 string encoding.

  Args:
    fig: A matplotlib Figure.

  Returns:
    A base64 encoding of the figure.
  """
  buf = io.BytesIO()
  fig.savefig(buf, bbox_inches='tight', format='png')
  return base64.b64encode(buf.getbuffer().tobytes()).decode('ascii')


def generate_fairness_log_completeness_label():
    """
    Generate a digital trust label as SVG and add it to the reports/README.md file.
    """
    import os
    import svg

    def calculate_log_completeness(log_path):
        """
        Calculate the completeness of fairness logs.

        Args:
        log_path: The path to the fairness log file.

        Returns:
        A float between 0 and 1 representing the completeness of fairness logs,
        where 1 is fully complete.
        """
        fairness_log_keys = ["sample_results", "variable_profile", "bygroup_metrics"]  # Define the expected fairness log keys
        fairness_log = load(log_path)
        fairness_log_keys_found = [key for key in fairness_log.keys() if key in fairness_log_keys]
        log_completeness = len(fairness_log_keys_found) / len(fairness_log_keys)
        print(f"We found the keys: {str(fairness_log_keys_found)}. Based on the log, the fairness log completeness is calculated: {log_completeness}")
        return log_completeness

    def generate_fairness_logo(log_completeness, output_filename="fairness_logo.svg"):
        """
        Generates an SVG fairness certification logo with dynamic color and shape
        based on the completeness of fairness logs.

        Args:
        log_completeness: A float between 0 and 1 representing the completeness
                of the fairness logs, where 1 is fully complete.
        output_filename: The name of the SVG file to save the logo.

        Returns:
        None. Saves the generated logo to an SVG file.
        """

        # Color Mapping (Example):
        hue = 270  # Hue for purple
        saturation = int(100 * log_completeness)  # Saturation based on log completeness
        lightness = 50  # Fixed lightness
        color_hsl = f'hsl({hue}, {saturation}%, {lightness}%)'

        canvas = svg.SVG(
            width=100, 
            height=100,
            elements = [
                svg.Circle(cx=50, cy=50, r=40 * log_completeness, fill=color_hsl, stroke='black', stroke_width=2)
            ]
        )
        
        with open(output_filename, 'w') as f:
            f.write(str(canvas))
        return canvas
    
    def add_label_to_readme(fairness_logo):
        """
        Add the fairness logo to the README file.
        """
        readme_file = "reports/README.md"
        if not os.path.exists(readme_file):
            with open(readme_file, 'w') as f:
                f.write("# Fairness Report Overview\n\n")
                f.write("This README contains the fairness report and related information.\n\n")

        with open(readme_file, 'a') as f:
            f.write(str(fairness_logo))
        return
    
    log_path = get_fairness_log_path()
    log_completeness = calculate_log_completeness(log_path)
    fairness_logo = generate_fairness_logo(log_completeness)
    add_label_to_readme(fairness_logo)
    return

class OntologyChart:
    def __init__(self):
        # Load the JSON data
        self.current_folder_location = os.path.dirname(os.path.abspath(__file__))

    
    def show_fairness_ontology_chart(self):
        with open(self.current_folder_location + "/schema/fairness_ontology.json", 'r') as file:
            data = json.load(file)
        fairness_notion = data['Fairness Notion']
        
        # Create a list to hold the chart data
        labels = []
        parents = []
        
        def add_to_chart(node, parent_label):
            for key, value in node.items():
                labels.append(key)
                parents.append(parent_label)
                if isinstance(value, dict):
                    add_to_chart(value, key)
        
        # Start with the root node
        add_to_chart(fairness_notion, "")
        
        # Create the hierarchical chart using Plotly
        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents
        ))
        
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        fig.show()