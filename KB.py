from horn_clause import *

class KB:
    def __init__(self):
        self.clauses = []
        self.facts = []
        self.query = None

    def parse_input_file(self, file_name):
        with open(file_name, "r") as f:
            content = f.read().split("ASK")

            tell_section = content[0].strip().replace("TELL", "").strip()

            # Parse the query
            self.query = content[1].strip()

            # Parse the TELL section
            sentences = tell_section.split(';')
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence:
                    if "=>" in sentence:
                        self.clauses.append(HornClause(sentence))
                    else:
                        self.facts.append(sentence)

    # Get all the propositional symbols
    def get_all_symbols(self):
        all_symbols = set(self.facts)

        for clause in self.clauses:
            all_symbols.update(clause.get_symbols())

        # all_symbols.add(self.query)

        return list(all_symbols)

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
