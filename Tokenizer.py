
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
