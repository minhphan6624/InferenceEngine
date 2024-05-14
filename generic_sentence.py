class GenericSentence:
    def __init__(self, sentence):
        self.original = sentence
        self.lhs = None
        self.rhs = None
        self.parse_sentence(sentence)

    def parse_sentence(self, sentence):
        if '<=>' in sentence:
            parts = sentence.split('<=>')
            self.lhs = parts[0].strip()  # Left-hand side (lhs)
            self.rhs = parts[1].strip()  # Right-hand side (rhs)
        elif '=>' in sentence:
            parts = sentence.split('=>')
            self.lhs = parts[0].strip()  # Left-hand side (lhs)
            self.rhs = parts[1].strip()  # Right-hand side (rhs)
        else:
            self.lhs = sentence.strip()  # No implication or biconditional, treat entire sentence as lhs