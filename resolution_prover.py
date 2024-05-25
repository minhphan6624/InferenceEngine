from Tokenizer import *
from GenericSentence import *

# Eliminate implications and biconditionals


# def eliminate_implications(tokens):
#     new_tokens = []
#     i = 0
#     while (i < len(tokens)):
#         token = tokens[i]

#         # Implications: a => b becomes ~(a || b)
#         if token == "=>":
#             new_tokens.append("~")
#             new_tokens.append(tokens[i-1])
#             new_tokens.append("||")
#             new_tokens.append(tokens[i+1])
#         # Biconditionals: A <=> B becomes (~A || B) & (~B || A)
#         elif token == "<=>":
#             converted = ['(', '~', tokens[i-1], '||', tokens[i+1], ')',
#                          '&', '(', '~', tokens[i+1], '||', tokens[i-1], ')']
#             new_tokens.extend(converted)
#         else:
#             new_tokens.append(token)

#         i += 1

#     return new_tokens

# def eliminate_implications(tokens):
#     new_tokens = []
#     i = 0
#     while i < len(tokens):
#         token = tokens[i]
#         if token == "=>":
#             # Start by adding the negation and a parenthesis to handle complex left-hand expressions
#             new_tokens.extend(['~', '('])
#             # Include all tokens that make up the left-hand side expression
#             lhs_start = i - 1
#             while lhs_start > 0 and not is_operator(tokens[lhs_start - 1]):
#                 lhs_start -= 1
#             new_tokens.extend(tokens[lhs_start:i])
#             new_tokens.append(')')
#             new_tokens.append('||')
#             # Now handle the right-hand side expression
#             rhs_end = i + 2
#             while rhs_end < len(tokens) and not is_operator(tokens[rhs_end]):
#                 rhs_end += 1
#             new_tokens.extend(tokens[i+1:rhs_end])
#         elif token == "<=>":
#             # Biconditionals handled similarly with adjustments for both directions
#             lhs_start = i - 1
#             rhs_end = i + 2
#             while lhs_start > 0 and not is_operator(tokens[lhs_start - 1]):
#                 lhs_start -= 1
#             while rhs_end < len(tokens) and not is_operator(tokens[rhs_end]):
#                 rhs_end += 1
#             lhs = tokens[lhs_start:i]
#             rhs = tokens[i+1:rhs_end]
#             converted = ['(', '~'] + lhs + ['||'] + rhs + [')', '&&', '(', '~'] + rhs + ['||'] + lhs + [')']
#             new_tokens.extend(converted)
#         else:
#             new_tokens.append(token)
#         i = rhs_end if token in ["=>", "<=>"] else i + 1

#     return new_tokens

# def is_operator(token):
#     return token in ['&&', '||', '~', '=>', '<=>']

def eliminate_implications(tokens):
    if not tokens:
        return []
    if '=>' in tokens:
        return handle_implication(tokens, '=>', lambda l, r: ['~'] + ['('] + l + [')'] + ['||'] + r)
    elif '<=>' in tokens:
        return handle_implication(tokens, '<=>', lambda l, r: ['('] + ['~'] + l + ['||'] + r + [')'] + ['&&'] + ['('] + ['~'] + r + ['||'] + l + [')'])
    else:
        return tokens  # Base case: no implications to handle

def handle_implication(tokens, operator, transform_func):
    # Split the token list at the operator
    op_index = tokens.index(operator)
    left_expr = eliminate_implications(tokens[:op_index])  # Recursively handle the left side
    right_expr = eliminate_implications(tokens[op_index + 1:])  # Recursively handle the right side

    # Transform the expression around the operator
    return transform_func(left_expr, right_expr)


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
