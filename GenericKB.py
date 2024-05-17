from GenericSentence import *
import re

class GenericKB:
    def __init__(self):
        self.facts = []
        self.generic_sentences = []
        self.query = None

    def parse_input(self, sentences, query):
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                if re.search(r'[<=>&|~()]', sentence):
                    self.generic_sentences.append(GenericSentence(sentence))
                else:
                    self.facts.append(sentence)
        self.query = query


    # Get all the propositional symbols
    def get_all_symbols(self):

        symbols = set(self.facts)

        for sentence in self.generic_sentences:
            symbols.update(re.findall(r'\b\w+\b', sentence.original))
            
        if isinstance(self.query, GenericSentence):
            symbols.update(re.findall(r'\b\w+\b', self.query.original))
        else:
            symbols.add(self.query)

        return list(symbols)
    
    def display(self):
        print("Facts:")
        for fact in self.facts:
            print(f"{fact}")
        print("\nGeneric Sentences:")
        for sentence in self.generic_sentences:
            sentence.display()
        print("Query:")
        if isinstance(self.query, str):
            print(self.query)
        else:
            self.query.display()