import re


class GenericSentence:
    def __init__(self, sentence):
        cleaned_sentence = sentence.strip().replace(" ", "")
        self.original = cleaned_sentence

    def evaluate(self, model):
        return self.evaluate_expression(self.original, model)

    def evaluate_expression(self, expression, model):
        # Handle parentheses by evaluating subexpressions recursively
        print(f"Evaluating expression: {expression} with model: {model}")
        while '(' in expression:
            sub_expr = re.search(r'\([^()]*\)', expression).group()
            print(f"Found subexpression: {sub_expr}")
            sub_value = self.evaluate_expression(sub_expr[1:-1], model)
            expression = expression.replace(sub_expr, str(sub_value), 1)
            print(f"Expression after substitution: {expression}")

        # Split the expression into terms and operators using regex
        terms = re.split(r'\s*(&|\|\||~|<=>|=>)\s*', expression)
        # terms = re.split(r'(?<=[a-zA-Z0-9])(?=[~|=&<>])|(?<=[~|=&<>])(?=[a-zA-Z0-9])', expression)

        print(f"Split terms and operators: {terms}")
        result = None

        # Check for initial negation
        if terms[0] == '~':
            if terms[1] == 'True':
                result = False
            if terms[1] == 'False':
                result = True
            else:
                result = not model.get(terms[0], False)
                print(f"Initial negation: ~{terms[1]} results in {result}")
            terms = terms[2:]  # Skip over the negated term and its operator
        else:
            if terms[0] == 'True':
                result = True
            elif terms[0] == 'False':
                result = False
            else:
                result = model.get(terms[0], False)  # Initial term value
                print(f"Initial term: {terms[0]} evaluated to {result}")

        # Iterate over the operators and terms
        i = 1
        while i < len(terms):
            operator = terms[i]
            next_term = terms[i + 1]

            # Check for negation of the next term
            if next_term == '~':
                if terms[i + 2] == 'True':
                    next_value = False
                elif terms[i + 2] == 'False':
                    next_value = True
                else:
                    next_value = not model.get(terms[i + 2], False)
                i += 3  # Move past the negated term
            else:
                if next_term == 'True':
                    next_value = True
                elif next_term == 'False':
                    next_value = False
                else:
                    next_value = model.get(next_term, False)
                i += 2  # Move past the term

            # Apply the operator
            if operator == '&':
                result = result and next_value
            elif operator == '||':
                result = result or next_value
            elif operator == '=>':
                result = not result or next_value
            elif operator == '<=>':
                result = result == next_value
            print(
                f"After applying operator {operator} with {next_term}: result is {result}")

        print(f"Final result of expression evaluation: {result}")
        return result

    def display(self):
        print(f"Original: {self.original}")
        print()
        tokenizer = Tokenizer(self.original)
        tokens = tokenizer.tokenize()
        print(tokens)
        print(shunting_yard(tokens))
        print()

# Break the input into managable pieces (tokens)


class Tokenizer:
    def __init__(self, expression):
        self.expression = expression
        self.position = 0
        self.length = len(expression)

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
        if token.isalnum():  # token is an operand
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
