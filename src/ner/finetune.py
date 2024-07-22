# %%
import os
import json
import random
import spacy
from spacy.tokens import DocBin
from spacy.training import Example
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from annotate import annotate_text

# %% Load the nnotation data
def load_annotation_finetune_data(file_path):
    """
    Load the annotation data from the JSON file
    file_path: str - The path to the JSON file
    Returns: The annotation data as a list
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# %% Create spaCy DocBin objects from the annotated data
def create_docbin(data):
    """
    Create spaCy DocBin objects from the annotated data
    data: list - The annotated data
    Returns: The spaCy DocBin object
    """
    db = DocBin()

    # Iterate through the data
    for text, annot in tqdm(data):
        doc = annotate_text(text)
        annot = annot['entities']

        ents = []
        entity_indices = []

        # Extract entities from the annotations
        for start, end, label in annot:
            skip_entity = False
            for idx in range(start, end):
                if idx in entity_indices:
                    skip_entity = True
                    break
            if skip_entity:
                continue

            entity_indices = entity_indices + list(range(start, end))
            try:
                span = doc.char_span(start, end, label=label, alignment_mode='strict')
            except:
                continue

            if span is None:
                # Log errors for annotations that couldn't be processed
                err_data = str([start, end]) + "    " + str(text) + "\n"
                print(f"Skipping entity: {err_data}")
            else:
                ents.append(span)

            try:
                doc.ents = ents
                db.add(doc)
            except:
                pass
    
    return db

# %% Generate training and testing data
def generate_training_test_data(annotation_filepath):
    """
    Generate training and testing data from the annotation file
    """
    training_data = load_annotation_finetune_data(annotation_filepath)
    train, test = train_test_split(training_data, test_size=0.2)

    try:
        os.makedirs('data/annotation')
    except FileExistsError:
        pass
    
    db = create_docbin(train)
    db.to_disk('data/annotation/train_data.spacy')

    db = create_docbin(test)
    db.to_disk('data/annotation/test_data.spacy')
    print("Training and testing data generated successfully. The files are saved to 'data/annotation'.")
    return train, test

# %% train_ner_model
def train_ner_model(train_data_path, model_path, n_iter=100):
    """
    Train the NER model using the training data
    train_data_path: str - The path to the training data
    model_path: str - The path to save the model
    n_iter: int - The number of iterations to train the model
    """

    if not os.path.exists(train_data_path):
        print("Training data not found. Please generate the training data first.")

    nlp = spacy.blank("en")
    nlp.add_pipe("ner", last=True)
    data = DocBin().from_disk(train_data_path)
    TRAIN_DATA = []
    for doc in data.get_docs(nlp.vocab):
        entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        example = Example.from_dict(doc, {"entities": entities})
        TRAIN_DATA.append(example)

    # Train the NER model
    losses = {}
    with nlp.select_pipes(enable=["ner"]):
        optimizer = nlp.begin_training()
        for _ in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for example in TRAIN_DATA:
                nlp.update([example], drop=0.5, sgd=optimizer,losses=losses)
            print(losses)

    # Save the model
    if not os.path.exists(model_path):
        print("Model path not found. Creating the directory.")
        os.makedirs(model_path)
    nlp.to_disk(model_path)
    print("Model trained successfully and saved to: " + model_path)

    return nlp

# %% Test cases
"""
training_data, test_data = generate_training_test_data('../../data/annotation/annotations.json')
training_data[0]

# %% Start training the model
custom_model = train_ner_model('../../data/annotation/train_data.spacy', '../../data/annotation/model-custom', n_iter=25)

# %% Test the model
for text, _ in test_data:
    doc = custom_model(text)
    print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
    print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

"""