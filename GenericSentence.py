import re

class GenericSentence:
    def __init__(self, sentence):
        self.original = sentence.strip()

    def evaluate(self, model):
        return self.evaluate_expression(self.original, model)

    def evaluate_expression(self, expression, model):
        # Handle parentheses by evaluating subexpressions recursively
        while '(' in expression:
            sub_expr = re.search(r'\([^()]*\)', expression).group()
            sub_value = self.evaluate_expression(sub_expr[1:-1], model)
            expression = expression.replace(sub_expr, str(sub_value))

        # Split the expression into terms and operators using regex
        terms = re.split(r'\s*(&|\|\||~|<=>|=>)\s*', expression)
        result = None

        # Check for initial negation
        if terms[0] == '~':
            if terms[1] == 'True':
                result = False
            if terms[1] == 'False':
                result = True
            else:
                result = not model.get(terms[0], False)
            terms = terms[2:] #Skip over the negated term and its operator
        else:
            if terms[0] == 'True':
                result = True
            elif terms[0] == 'False':
                result = False
            else:
                result = model.get(terms[0], False)  # Initial term value   

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

        return result
    
    def display(self):
        print(f"Original: {self.original}")
        print()
    