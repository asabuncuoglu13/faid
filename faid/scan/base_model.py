# %%
from ..logging.message import error_msg

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
# %% test use case
# html_out = get_fairness_score(get_base_model_name_from_hf("NousResearch/Llama-2-13b-hf"), html=True)
