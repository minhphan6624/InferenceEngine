from sympy.logic.boolalg import Or, And, Not
from sympy import symbols, Or, And, Not, Implies, Equivalent, to_cnf
from Tokenizer import *
from GenericSentence import *


def create_sympy_expr(tokens):
    """
    Convert a list of tokens in RPN into a SymPy expression.
    tokens: List of strings, where operators are '||', '&', '~', '=>', '<=>'
    and other elements are variable names.
    """
    # Mapping from token to SymPy function
    op_map = {
        '||': Or,
        '&': And,
        '~': Not,
        '=>': Implies,
        '<=>': Equivalent
    }

    stack = []

    for token in tokens:
        if token in op_map:
            if token == '~':  # Unary operator
                operand = stack.pop()
                result = op_map[token](operand)
            else:  # Binary operators
                right = stack.pop()
                left = stack.pop()
                result = op_map[token](left, right)
            stack.append(result)
        else:
            stack.append(symbols(token))

    return stack.pop() if stack else None

# Convert a list of tokens in RPN to Sympy cnf


def convert_to_cnf(tokens):
    expr = create_sympy_expr(tokens)

    return to_cnf(expr, simplify=True)

# ------------------ Parsing a sympy CNF expression ----------------------

# Parse a SymPy CNF expression to get the clauses


def parse_cnf(cnf_expression):
    if isinstance(cnf_expression, And):
        return [frozenset(parse_clause(c)) for c in cnf_expression.args]
    else:
        return [frozenset(parse_clause(cnf_expression))]


def parse_clause(clause):
    if isinstance(clause, Or):
        return [parse_literal(lit) for lit in clause.args]
    else:
        return [parse_literal(clause)]


def parse_literal(literal):
    if isinstance(literal, Not):
        return f"~{str(literal.args[0])}"
    else:
        return str(literal)


# -------------- Resolution prover ------------------

# Resolve a list of clauses
def resolve(clauses):
    new = set()
    # Convert the set to a list for pairing
    clause_list = list(clauses)

    # Loop through each pair of clauses using indices in the list
    for i in range(len(clause_list)):
        for j in range(i + 1, len(clause_list)):
            ci = clause_list[i]
            cj = clause_list[j]

            # For each literal in one clause
            for x in ci:
                # Check if its complement is in the other
                if f"~{x}" in cj or (x.startswith("~") and x[1:] in cj):
                    new_clause = frozenset(
                        (ci | cj) - {x, f"~{x}" if not x.startswith("~") else x[1:]})

                    if new_clause == frozenset():
                        return True, None  # Found empty clause, return True

                    new.add(frozenset(new_clause))
    return False, new

# Main resolution prover driver code


def resolution_prover(cnf_expression):
    # Ensure clauses are a set of frozensets
    clauses = set(parse_cnf(cnf_expression))
    while True:
        contradiction, new_clauses = resolve(clauses)
        if contradiction:
            return "Unsatisfiable"
        # Ensure this is also a set of frozensets
        new_clauses_set = set(new_clauses)
        if new_clauses_set == clauses:  # Use == for set comparison
            return "Satisfiable"
        clauses.update(new_clauses_set)  # Properly updating the set


def res_entails(kb, query):

    cnf_kb = And(*[convert_to_cnf(sentence.to_rpn())
                 for sentence in kb.generic_sentences])

    cnf_kb = to_cnf(cnf_kb)

    print(cnf_kb)

    # cnf_query = convert_to_cnf(query.to_rpn())
    # negated_cnf_query = to_cnf(Not(cnf_query), simplify=True)

    # print(negated_cnf_query)

    # # Combine the CNF of the KB and the negated query
    # combined_cnf = And(cnf_kb, negated_cnf_query)

    # print(combined_cnf)

    # # Use your resolution solver
    # result = resolution_prover(combined_cnf)

    # return result == "Unsatisfiable"  # If unsatisfiable, KB entails the query
