from sympy import symbols, Or, And, Not, Implies, Equivalent, to_cnf
from Tokenizer import *
from GenericSentence import *
   
def create_sympy_expr(tokens):
    """
    Convert a list of tokens into a SymPy expression.
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

def convert_to_cnf(tokens):
    expr = create_sympy_expr(tokens)

    return to_cnf(expr, simplify=True)

def resolve(clause1, clause2):
    # Find complementary literals
    for literal in clause1:
        if -literal in clause2:  # Assuming literals are integers, negation is represented by negative numbers
            # Create a new clause by resolving the pair
            new_clause = (clause1 | clause2) - {literal, -literal}
            return new_clause
    return None

def resolution_solver(clauses):
    new_clauses = set()
    while True:
        for clause1 in clauses:
            for clause2 in clauses:
                if clause1 != clause2:
                    resolvent = resolve(clause1, clause2)
                    if resolvent is None:
                        continue
                    if not resolvent:  # Empty clause means contradiction
                        return False
                    new_clauses.add(frozenset(resolvent))
        if new_clauses.issubset(clauses):
            return True  # No new clauses, original formula is satisfiable
        clauses.update(new_clauses)

# Example usage
clauses = {frozenset([-1, -2, -3, 4])}  # Represents the CNF ~A ∨ ~B ∨ ~C ∨ D
result = resolution_solver(clauses)
print("Satisfiable:", result)

