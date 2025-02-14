# %%
import random
import nltk
import re

# %%
class CounterfactualGenerator:

    @staticmethod
    def split_alpha_numeric(tokens):
        split_tokens = []
        for token in tokens:
            # Split the token into alphabetic and numeric parts
            parts = re.findall(r'[A-Za-z]+|\d+', token)
            split_tokens.extend(parts)
        return split_tokens

    def __init__(self, vocab:list):
        nltk.download('punkt')
        self.vocabulary = vocab
        self.vocabulary = [str(word).lower() for word in self.vocabulary]

    def generate_random_counterfactual(self, sentence):
        """
        Generate counterfactual text by replacing target words with random words from the same vocabulary.
        self.vocabulary: list of target words
        sentence: input sentence
        Returns a single counterfactual sentence.
        """
        words = self.split_alpha_numeric(nltk.word_tokenize(sentence))
        counterfactual_words = []

        if len(words) == 0:
            return sentence

        for word in words:
            if word.lower() in self.vocabulary:
                replacement = random.choice(self.vocabulary)
                while replacement == word.lower():
                    replacement = random.choice(self.vocabulary)
                counterfactual_words.append(replacement)
            else:
                counterfactual_words.append(word)

        return ' '.join(counterfactual_words)

    def generate_counterfactuals(self, sentence):
        """
        Generate counterfactual text by replacing target words with random words from the same vocabulary.
        """
        words = self.split_alpha_numeric(nltk.word_tokenize(sentence))
        
        counterfactual_sentences = []

        if len(words) == 0:
            return sentence
        
        for candidate in self.vocabulary:
            counterfactual_words = []
            for word in words:
                if word.lower() in self.vocabulary:
                    counterfactual_words.append(candidate)
                else:
                    counterfactual_words.append(word)

            counterfactual_sentences.append(' '.join(counterfactual_words))
        
        return counterfactual_sentences
    

# %% Test the CounterfactualGenerator class
"""
df = pd.read_csv('data/codes-all.csv')
vocabulary = df['Entity'].tolist()
cf_generator = CounterfactualGenerator(vocabulary)
sentence = "ARGENTINA 1-0 NETHERLANDS"
print(cf_generator.generate_random_counterfactual(sentence))
"""
# %%
