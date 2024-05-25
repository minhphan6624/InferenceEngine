from Tokenizer import *
from GenericSentence import *

# Eliminate implications and biconditionals


def eliminate_implications(tokens):
    new_tokens = []
    i = 0
    while (i < len(tokens)):
        token = tokens[i]

        # Implications: a => b becomes ~(a || b)
        if token == "=>":
            new_tokens.append("~")
            new_tokens.append(tokens[i-1])
            new_tokens.append("||")
            new_tokens.append(tokens[i+1])
        # Biconditionals: A <=> B becomes (~A || B) & (~B || A)
        elif token == "<=>":
            converted = ['(', '~', tokens[i-1], '||', tokens[i+1], ')',
                         '&', '(', '~', tokens[i+1], '||', tokens[i-1], ')']
            new_tokens.extend(converted)
        else:
            new_tokens.append(token)

        i += 1

    return new_tokens


def move_negation_inwards(tokens):
    stack = []

    i = 0

    while (i < len(tokens)):
        if (tokens[i] == '~' and tokens[i+1] == '(') or tokens[i] == '(':
            stack.append(tokens[i])
        elif tokens[i] in ["||", "&"]:
            if stack and stack[i-1] == '~':
                stack.pop()
        else:  # Append all other operators and operands
            stack.append(tokens[i])

        i += 1


def ditribute_and_over_or():
    pass


def to_cnf(sentence):
    tokenizer = Tokenizer(sentence.original)

    tokens = tokenizer.tokenize()

    tokens = eliminate_implications(tokens)
