import os
import json
import plotly.graph_objects as go

class OntologyChart:
    def __init__(self):
        # Load the JSON data
        self.current_folder_location = os.path.dirname(os.path.abspath(__file__))

    
    def add_fairness_ontology_chart(self):
        with open(self.current_folder_location + "/schema/fairness_ontology.json", 'r') as file:
            data = json.load(file)
        fairness_notion = data['FairnessNotion']
        
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

    def add_model_card_viz(self):
        with open(self.current_folder_location + "/schema/model_card.json", 'r') as file:
            data = json.load(file)
        model_card = data["properties"]
        
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
        add_to_chart(model_card, "")
        
        # Create the hierarchical chart using Plotly
        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents
        ))
        
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        fig.show()