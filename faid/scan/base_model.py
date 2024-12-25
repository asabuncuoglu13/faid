# %%
from faid.logging import error_msg

# %%
def get_base_model_name_from_hf(model_name: str):
    from huggingface_hub import ModelCard
    card = ModelCard.load(model_name)

    if card.data['base_model']:
        print(f'Base model information from HF model card metadata: {card.data["base_model"]}')
        return card.data['base_model']
    else:
        from transformers import AutoConfig
        config = AutoConfig.from_pretrained(model_name)
        if not config.model_type:
            error_msg(f'Could not find base model for {model_name}')
        print(f'Base model information from HF config: {config.model_type}')
        return config.model_type
    

# %%
def get_fairness_score(model_name: str, html=False):
    import pandas as pd
    from thefuzz import fuzz
    from thefuzz import process

    path = __file__.replace('base_model.py', '../data/HELM-Fairness.csv')
    benchmark = pd.read_csv(path)
    model_names = benchmark['Model'].unique()

    scorer = fuzz.ratio
    closest = process.extractOne(model_name, model_names, scorer=scorer)
    if closest[1] > 60:
        scores = benchmark[benchmark['Model'] == closest[0]]
        from tabulate import tabulate
        print(tabulate(scores, headers='keys', tablefmt='psql'))
        if html:
            return tabulate(scores, headers='keys', tablefmt='html')
        return scores
    else:
        print(f'Could not find a fairness score for {model_name}. Check https://crfm.stanford.edu/helm/ (Stanford HELM Leaderboard) for a list of models')
        return None
    
# %%
def get_fairness_metric_explanations():
    import pandas as pd

    path = __file__.replace('base_model.py', '../data/evals.csv')
    benchmark = pd.read_csv(path)

    return benchmark

# %% display benchmark as a dropdown html

def fairness_benchmark_dropdown():

    df = get_fairness_metric_explanations()

    html_code = """
    <select id="dropdown" onchange="displayDetails()">
        <option value="">Select an option</option>
    """
    for idx, row in df.iterrows():
        html_code += f'<option value="{idx}">{row[0]}</option>\n'

    html_code += """
    </select>

    <div id="details"></div>

    <script type="text/javascript">
    function displayDetails() {
        var data = %s;
        var selectedIndex = document.getElementById('dropdown').value;
        var detailsDiv = document.getElementById('details');

        if (selectedIndex === "") {
            detailsDiv.innerHTML = "";
            return;
        }

        var details = data[selectedIndex];
        var html = "<ul>";
        for (var key in details) {
            if (key !== 'Option') {
                html += "<li><strong>" + key + ":</strong> " + details[key] + "</li>";
            }
        }
        html += "</ul>";

        detailsDiv.innerHTML = html;
    }
    </script>
    """ % df.to_dict(orient='index')

    # check if Ipython is available
    try:
        get_ipython()
    except NameError:
        print("In Jupyter Notebook, this function displays the dropdown menu. In other environments, it returns the HTML code.")
        return html_code
    else:
        from IPython.display import display, HTML, Javascript
        display(HTML(html_code))

# %% test use case
# html_out = get_fairness_score(get_base_model_name_from_hf("NousResearch/Llama-2-13b-hf"), html=True)


# %%
