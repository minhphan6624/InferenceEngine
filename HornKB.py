from HornClause import *
from GenericSentence import *
import re

class HornKB:
    def __init__(self):
        self.clauses = []
        self.facts = []
        self.query = None

    # Parse input for a horn KB 
    def parse_input(self, sentences, query):
        # Parse the TELL section
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                if "=>" in sentence:
                    self.clauses.append(HornClause(sentence))
                else:
                    self.facts.append(sentence)

        self.query = query

    # Get all the propositional symbols
    def get_all_symbols(self):
        all_symbols = set(self.facts)

        for clause in self.clauses:
            all_symbols.update(clause.get_symbols())

        return list(all_symbols)

    #Display for bebuggig purposes
    def display(self):
        print("Facts:")
        for fact in self.facts:
            print(fact)
        print(len(self.facts))
        print("Clauses:")
        for clause in self.clauses:
            clause.display()
        print("Query:")
        print(self.query)
