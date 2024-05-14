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
    return not premise_true or conclusion_true

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


def truth_table_check(kb, query):

    symbols = kb.get_all_symbols()

    models = generate_models(symbols)

    entailed = False
    count = 0

    for model in models:
        symbol_model = dict(zip(symbols, model))

        # Check for models where KB is true
        if evaluate_kb(kb, symbol_model):
            count += 1
            if not evaluate_fact(query):
                entailed = False

    return ("YES", count) if entailed else ("NO", count)
