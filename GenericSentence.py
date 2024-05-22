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

# Break the input into managable pieces (tokens)


class Tokenizer:
    def __init__(self, expression):
        self.expression = expression
        self.position = 0
        self.length = len(expression)

    # Get the next token in the expression
    def get_next_token(self):
        while self.position < self.length and self.expression[self.position].isspace():
            self.position += 1

        if self.position >= self.length:
            return None  # End of string

        # Processing multi-character operators
        # 2-character operators
        if self.position + 1 < self.length:
            two_char = self.expression[self.position:self.position+2]
            if two_char in ['=>', '||', '&&']:
                self.position += 2
                return two_char

        # 3-charcter operator i.e. <=>
        if self.position + 2 < self.length:
            three_char = self.expression[self.position:self.position+3]
            if three_char == '<=>':
                self.position += 3
                return three_char

        # Single character tokens (operators and parentheses)
        current_char = self.expression[self.position]
        self.position += 1
        if current_char in '()~|&=':
            # Handles all single character operators including parentheses and negation
            return current_char

        # Handle variables and other alphabets as operands
        if current_char.isalpha():
            start = self.position - 1
            while self.position < self.length and self.expression[self.position].isalpha():
                self.position += 1
            return self.expression[start:self.position]

        return current_char

    def tokenize(self):
        tokens = []
        token = self.get_next_token()
        while token:
            tokens.append(token)
            token = self.get_next_token()
        return tokens

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


# Evaluate an expression in RPN (Postfix representation)
def evaluate_rpn(expression, model):
    stack = []
    for token in expression:
        if token.isalnum():  # operand
            # Retrieve the boolean value from the model
            stack.append(model.get(token, False))
        else:  # operator
            if token == '~':
                operand = stack.pop()
                stack.append(not operand)
            else:
                right = stack.pop()
                left = stack.pop()
                if token == '&':
                    stack.append(left and right)
                elif token == '||':
                    stack.append(left or right)
                elif token == '=>':
                    stack.append(not left or right)
                elif token == '<=>':
                    stack.append(left == right)

    return stack.pop()
