# %%
import spacy
from spacy import displacy

NER = spacy.load("en_core_web_sm")

# %% Annotate the text
def annotate_text(text, model_path=None):
    """
    Annotate the text using the spaCy model
    text: str - The text to be annotated
    model_path: str - The path to the custom model
    Returns: The annotated text as a spaCy doc object
    """
    if model_path is None:
        doc = NER(text)
    else:
        ner_model = spacy.load(model_path)
        doc = ner_model(text)
    return doc

# %% Load the spaCy model
def display_annotated_text_visual(text, model_path=None):
    """
    Display the annotated text in a visual format using spacy's built-in renderer
    text: str - The text to be annotated
    model_path: str - The path to the custom model
    """
    doc = annotate_text(text, model_path)
    displacy.render(doc, style="ent", jupyter=True)

# %% Get the annotated text
def get_annotated_text(text, model_path=None):
    """
    Get the annotated text
    text: str - The text to be annotated
    model_path: str - The path to the custom model
    Returns: A list of tuples containing the annotated text and the entity label
    """
    doc = annotate_text(text, model_path)
    annotated_text = []
    for ent in doc.ents:
        annotated_text.append((ent.text, ent.label_))
    return annotated_text

# %% Annotate the prompts with the custom model
def get_entity_counts_from_annotated_text(prompts_df, prompt_clm_name, model_path=None):
    """
    Annotate the prompts with the custom model
    prompts_df: DataFrame - The DataFrame containing the prompts line-by-line
    prompt_clm_name: str - The column name of the prompts
    model_path: str - The path to the custom model
    Returns: A dictionary containing the counts of the entities
    """
    entity_counts = {}
    
    for i in range(len(prompts_df)):
        text = prompts_df[prompt_clm_name][i]
        doc = annotate_text(text, model_path)
        
        for ent in doc.ents:
            entity_counts[ent.label_] += 1
                
    return dict(entity_counts)

# %% Test the functions
"""
text = "Apple is looking at buying U.K. startup for $1 billion"
print(get_annotated_text(text))
display_annotated_text_visual(text)
import pandas as pd
model = "../../data/annotation/model-best"
prompts_df = pd.read_csv("../../data/credit_prompts_augmented.csv")
prompt_clm_name = "Prompt"
entity_counts = get_entity_counts_from_annotated_text(model, prompts_df, prompt_clm_name)
"""
# %%
