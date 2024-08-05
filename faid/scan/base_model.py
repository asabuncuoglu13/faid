# %%
from ..utils.logging.message import error_msg

# %%
def get_base_model_name_from_hf(model_name: str):
    from huggingface_hub import ModelCard
    card = ModelCard.load(model_name)

    if card.data['base_model']:
        print(str(card.data['base_model']))
        return card.data['base_model']
    else:
        from transformers import AutoConfig
        config = AutoConfig.from_pretrained(model_name)
        if not config.model_type:
            error_msg(f'Could not find base model for {model_name}')
        return config.model_type
    

# %%
def get_fairness_score(model_name: str):
    import pandas as pd
    from thefuzz import fuzz
    from thefuzz import process

    benchmark = pd.read_csv('../data/HELM-Fairness.csv')
    model_names = benchmark['Model'].unique()

    scorer = fuzz.ratio
    closest = process.extractOne(model_name, model_names, scorer=scorer)
    print(f'Closest model: {closest[0]} with score {closest[1]}')
    if closest[1] > 60:
        scores = benchmark[benchmark['Model'] == closest[0]]
        return scores
    else:
        return None
# %% test use case
#get_fairness_score(get_base_model_name_from_hf("NousResearch/Llama-2-13b-hf"))

