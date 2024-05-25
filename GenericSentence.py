import re


class GenericSentence:
    def __init__(self, sentence):
        cleaned_sentence = sentence.strip().replace(" ", "")
        self.original = cleaned_sentence

    def get_symbols(self):
        # Get all the prop symbol in the generic sentence
        symbols = set(re.findall(r'\b[a-z]\b', self.original))
        return symbols

    # Display method for debugging purposes
    def display(self):
        print(f"Original: {self.original}")
