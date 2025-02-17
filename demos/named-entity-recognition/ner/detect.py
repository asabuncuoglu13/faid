from dataclasses import dataclass
from csv import DictReader
from typing import List, Union, Dict, Tuple

import spacy
from spacy import displacy

NER = spacy.load("en_core_web_sm")

# Create a new data class to represent the biased language row
@dataclass
class BiasedLanguage:
    """Dataclass of biased language to search for; automatically generated from the
    wordlist csv.
    """
    word: str
    dependent: Union[str, bool]
    alternative_words: Union[str, List[str]]
    example: str
    dependencies: Union[str, List[str]]

    def __post_init__(self):
        # Handle empty objects
        if self.dependencies == "":
            self.dependencies = None

        # Convert alt words & objects into list of words instead of one big string
        if isinstance(self.alternative_words, str):
            self.alternative_words = [
                word.strip() for word in self.alternative_words.split(",")
            ]
        if self.dependencies and isinstance(self.dependencies, str):
            if self.dependencies:
                self.dependencies = [d.strip() for d in self.dependencies.split(",")]

        # Convert string boolean values to true boolean
        if not isinstance(self.dependent, bool):
            if self.dependent.lower() in ["true", "t", "y", "yes"]:
                self.dependent = True
            elif self.dependent.lower() in ["false", "f", "n", "no"]:
                self.dependent = False
            else:
                raise ValueError(
                    f"Value for dependent ({self.dependent}) "
                    f"cannot be mapped to boolean."
                )

        # TODO: Check to see if input is actually in lemma form?

# 
@dataclass
class BiasedLanguageMatch:
    """Dataclass to store match results and associated wordlist data."""

    text: str
    lemma: str
    start: int
    end: int
    data: BiasedLanguage

    def __repr__(self):
        return self.text
    
def get_biased_words(word_list_path:str):
    biased_words = {}
    with open(word_list_path, "r") as wordlist_csv:
        reader = DictReader(wordlist_csv)
        for row in reader:
            row_data = BiasedLanguage(**row)
            biased_words[row_data.word] = row_data
    return biased_words
    

def match_biased_words(
    spacy_doc: spacy.tokens.Doc,
    biased_words: Dict[str, BiasedLanguage],
) -> List[spacy.tokens.Span]:
    """Given a document and a collection of biased word data objects, return the
    doc spans that match any of the biased words. Do not check for grammatical
    objects.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spacy doc
    biased_words: Dict[str, BiasedLanguage]
        Collection of biased words to search for, where the key is the string
        representation of the word and the value is the dataclass object containing
        the word's data

    Returns
    -------
    List[spacy.tokens.Span]
        Matched spans
    """
    matcher = spacy.matcher.Matcher(NER.vocab)
    matcher.add(
        "bword_rule",
        [
            [
                {
                    "LEMMA": {"IN": list(biased_words.keys())},
                    "POS": "VERB",
                    "DEP": {"NOT_IN": ["aux", "auxpass", "neg"]},
                },
            ]
        ],
    )
    #TODO: Add more rules to match other types not only VERB.

    bword_matches = [spacy_doc[start:end] for _, start, end in matcher(spacy_doc)]
    return bword_matches


def match_dependent_biased_words(
    spacy_doc: spacy.tokens.Doc,
    biased_words: Dict[str, BiasedLanguage],
    return_search_words: bool = False,
) -> Union[List[spacy.tokens.Span], List[Tuple[spacy.tokens.Span, spacy.tokens.Span]]]:
    """Given a document and a collection of biased word data objects that are
    dependent on the word-object relationship, return the doc spans that match any of
    the biased words and their grammatical objects.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spacy doc
    biased_words : Dict[str, BiasedLanguage]
        Collection of biased words to search for, where the key is the string
        representation of the word and the value is the dataclass object containing
        the word's data
    return_search_words : bool, optional
        If true, return a tuple where the first element is the original search term
        and the second is the matched results. If false, return the matched results
        only, by default False

    Returns
    -------
    Union[List[spacy.tokens.Span], List[Tuple[spacy.tokens.Span, spacy.tokens.Span]]]
        Matched spans or tuple containing the search term and matched spans
    """
    matcher = spacy.matcher.DependencyMatcher(NER.vocab)
    dep_obj_pattern = []
    for bword, word_data in biased_words.items():
        # dependencymatcher docs: https://spacy.io/api/dependencymatcher
        pattern = [
            # pattern always starts with a "right_id" anchor, which is the bword
            {"RIGHT_ID": f"anchor_{bword}", "RIGHT_ATTRS": {"LEMMA": bword}},
            # match direct dependencies of the bword
            {
                "LEFT_ID": f"anchor_{bword}",
                "REL_OP": ">",  # looks for the head relationship
                "RIGHT_ID": f"{bword}_object",
                "RIGHT_ATTRS": {"DEP": "dobj", "LEMMA": {"IN": word_data.dependencies}},
            },
        ]
        dep_obj_pattern.append(pattern)
    matcher.add("dep_word_rule", dep_obj_pattern)
    # return the entire span from bword to object, which includes any interim modifiers
    matches = matcher(spacy_doc)
    if return_search_words:
        return [
            (spacy_doc[token_ids[0]], spacy_doc[min(token_ids) : max(token_ids) + 1])
            for _, token_ids in matches
        ]
    else:
        return [
            spacy_doc[min(token_ids) : max(token_ids) + 1] for _, token_ids in matches
        ]


def find_biased_language(
    text: str,
    biased_word_list_path: str
) -> List[BiasedLanguage]:
    """For a given text document, return a list of the matched bias
    language phrases.

    Parameters
    ----------
    text : str
        The text to be analysed

    Returns
    -------
    List[BiasedLanguageMatch]
        List of matched biased language in the form of BiasedLanguageMatch dataclass
        instances
    """
    # Read in jd and convert to spacy doc
    ner_doc = NER(text)

    matched_results = []

    BIASED_WORDS = get_biased_words(biased_word_list_path)
    # Match words in bword list
    biased_words_non_obj_dep = {
        bword: bword_data
        for bword, bword_data in BIASED_WORDS.items()
        if not bword_data.dependent
    }
    for match in match_biased_words(ner_doc, biased_words_non_obj_dep):
        matched_results.append(
            BiasedLanguageMatch(
                lemma=match.lemma_,
                text=match.text,
                start=match.start,
                end=match.end,
                data=BIASED_WORDS[match.lemma_],
            )
        )

    # Match words that depend on dependencies, if present in the word list
    # A little repetitive, but need to use the original search term to access the data
    # in BiasedLanguage since these are phrases and not just exact matches
    biased_words_obj_dep = {
        bword: word_data
        for bword, word_data in BIASED_WORDS.items()
        if word_data.dependent
    }
    if len(biased_words_obj_dep) > 0:
        for search_word, match in match_dependent_biased_words(
            ner_doc, biased_words_obj_dep, return_search_words=True
        ):
            matched_results.append(
                BiasedLanguageMatch(
                    lemma=match.lemma_,
                    text=match.text,
                    start=match.start,
                    end=match.end,
                    data=BIASED_WORDS[search_word.lemma_],
                )
            )
    return matched_results

# Annotate the text
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

# Load the spaCy model
def display_annotated_text_visual(text, model_path=None):
    """
    Display the annotated text in a visual format using spacy's built-in renderer
    text: str - The text to be annotated
    model_path: str - The path to the custom model
    """
    doc = annotate_text(text, model_path)
    displacy.render(doc, style="ent", jupyter=True)

# Get the annotated text
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

# Annotate the prompts with the custom model
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