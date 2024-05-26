import re

from Tokenizer import *


class GenericSentence:
    def __init__(self, sentence):
        cleaned_sentence = sentence.strip().replace(" ", "")
        self.original = cleaned_sentence

    def get_symbols(self):
        # Get all the prop symbol in the generic sentence
        symbols = set(re.findall(r'\b[a-z]\b', self.original))
        return symbols

    def to_rpn(self):
        # Initialize a tokenizer for the sentence
        tokenizer = Tokenizer(self.original)

        # Get the list of tokens of the sentence
        tokens = tokenizer.tokenize()

        # Convert tokens into RPN
        rpn = shunting_yard(tokens)

        return rpn

    # Display method for debugging purposes
    def display(self):
        print(f"Original: {self.original}")


# Convert the list of tokens to Reverse Polish Notation (postfix)


def shunting_yard(tokens):
    # Operator precedence - operators with higher precedence are executed first
    precedence = {'~': 3, '&': 2, '||': 2, '=>': 1, '<=>': 1}

    associativity = {'~': 'right', '&': 'left',
                     '||': 'left', '=>': 'left', '<=>': 'left'}
    output = []  # Postfix(RPN) output queue
    operators = []  # operator stack

    for token in tokens:
        if token.isalnum():  # token is an operand (prop symbol)
            output.append(token)

        elif token in precedence:  # If token is an operator
            while (operators  # There are still operators on the stack...
                   # ..and there is no left parenthesis on top...
                   and operators[-1] != '('
                   and operators[-1] in precedence  # ...and
                   and (precedence[operators[-1]] > precedence[token]  # ...and the current operator has lower
                        or (precedence[operators[-1]] == precedence[token] and associativity[token] == 'left'))
                   ):
                output.append(operators.pop())
            operators.append(token)

        # Parenthesis handling
        elif token == '(':
            # Always push the opening parenthesis on to the stack
            operators.append(token)

        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()

    # After all tokens are parsed, flush the remaining operators on the stack onto the output queue
    while operators:
        output.append(operators.pop())
    return output
