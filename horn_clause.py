class HornClause:
    def __init__(self, sentence):

        split_by_entailment = sentence.split('=>')
        split_by_and = split_by_entailment[0].split('&')

        self.premise = [literal.strip() for literal in split_by_and]
        self.conclusion = split_by_entailment[1].strip()


    def get_literals(self):
        return self.premise



