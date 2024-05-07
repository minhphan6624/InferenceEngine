from horn_clause import *

class KB:
    def __init__(self, file_name):
        self.clauses = []
        self.facts = []
        if file_name:
                self.parse_input_file(file_name)


    def parse_input_file(self, file_name):
        with open(file_name, "r") as f:
            f.readline() #First line only contains "TELL"
        
            tell_sentences = f.readline().strip().split(";")

            for sentence in tell_sentences:
                sentence = sentence.replace(" ", "'") #Remove space inside a sentence
                if sentence.find("=>"):
                    self.clauses.append(HornClause(sentence))
                else:
                    self.facts.append(sentence)
