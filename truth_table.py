from KB import *
from itertools import *

# Generate all possible models based on a list of prop symbols


def generate_models(symbols):
    return list(product([True, False], repeat=len(symbols)))

# Truth-checking a fact in a model


def evaluate_fact(fact, model={}):
    return model.get(fact, False)

# Truth-checking a Horn Clause in a model


def evaluate_horn_clause(clause, model={}):
    premise_true = all(model.get(premise, False)
                       for premise in clause.premises)

    conclusion_true = model.get(clause.conclusion, False)

    # a => b <==> ~a v b
    return (not premise_true) or conclusion_true

# Check if the KB is true in a model


def evaluate_kb(kb, model={}):
    # Evaluate each fact
    for fact in kb.facts:
        if not evaluate_fact(fact, model):
            return False  # Short-circuit if any fact is false

    # Evaluate each clause
    for clause in kb.clauses:
        if not evaluate_horn_clause(clause, model):
            return False  # Short-circuit if any clause is false

    return True


def truth_table_check(kb, query):

    entailed = True
    count = 0

    #Generate all symbols
    symbols = kb.get_all_symbols()

    #Handling edge cases where query is not a symbol included in KB
    if query not in symbols:
        return ("NO", count)
    
    # Generate the models
    models = generate_models(symbols)

    for model in models:
        symbol_model = dict(zip(symbols, model))

        # Check for models where KB is true)
        if evaluate_kb(kb, symbol_model):
            count += 1
            #If the query is not true in that model
            if not evaluate_fact(query, symbol_model):
                entailed = False

    return ("YES", count) if entailed else ("NO", count)
