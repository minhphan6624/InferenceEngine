from sympy import symbols, Or, And, Not, Implies, Equivalent, to_cnf

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
    
    # Stack for storing expression parts
    expr_stack = []
    
    # Tokenize the expression properly (assuming RPN or similar)
    for token in tokens:
        if token in op_map:
            if token == '~':  # Unary operator
                arg = expr_stack.pop()
                expr_stack.append(op_map[token](arg))
            else:  # Binary operators
                right = expr_stack.pop()
                left = expr_stack.pop()
                expr_stack.append(op_map[token](left, right))
        else:
            # Convert proposition symbols to SymPy symbols
            expr_stack.append(symbols(token))
    
    # The expression stack should have one element, the complete expression
    return expr_stack[0] if expr_stack else None

def convert_to_cnf(tokens):
    """
    Converts a list of tokens directly to CNF using SymPy.
    """
    expr = create_sympy_expr(tokens)
    return to_cnf(expr, simplify=True)

# Example usage
tokens = ['A', 'B', '&', 'C', 'D', '||', '=>']
cnf_expr = convert_to_cnf(tokens)
print("CNF Expression:", cnf_expr)