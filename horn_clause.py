class HornClause:
    def __init__(self, clause):
        self.premises = []
        self.conclusion = None
        self.parse_clause(clause)

    def parse_clause(self, clause):
        parts = clause.split('=>')
        self.conclusion = parts[1].strip()
        self.premises = parts[0].strip().split('&')

    # Display function for debugging purposes
    def display(self):
        print(', '.join(self.premises),
              "=>", self.conclusion)

    # Get premise
    def get_premises(self):
        return self.premises

    # Get conclusion
    def get_conclusion(self):
        return self.conclusion

    # Get all the propositional symbols in the clause:
    def get_symbols(self):
        symbols = set()
        symbols.update(self.premises)
        symbols.update(self.conclusion)

        return symbols
