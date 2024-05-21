from HornKB import *
from itertools import *
import re

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


def evaluate_hornkb(kb, model={}):
    # Evaluate each fact
    for fact in kb.facts:
        if not evaluate_fact(fact, model):
            return False  # Short-circuit if any fact is false

    # Evaluate each clause
    for clause in kb.clauses:
        if not evaluate_horn_clause(clause, model):
            return False  # Short-circuit if any clause is false

    return True

# Main evaluation function for Horn KB


def truth_table_check_hornkb(kb, query):
    entailed = True
    count = 0

    # Generate all symbols
    symbols = kb.get_all_symbols()

    # Handling edge cases where query is not a symbol included in KB
    if query not in symbols:
        return ("NO", count)

    # Generate the models
    models = generate_models(symbols)
    for model in models:
        symbol_model = dict(zip(symbols, model))

        # Check for models where KB is true)
        if evaluate_hornkb(kb, symbol_model):
            count += 1
            # If the query is not true in that model
            if not evaluate_fact(query, symbol_model):
                entailed = False

    return ("YES", count) if entailed else ("NO", count)

# --------------- Generic KB ---------------------

# Check truth value of a generic sentence


def evaluate_generic_sentences(sentence, model={}):
    return sentence.evaluate(model)

# Check truth value of a generic KB


def evaluate_generic_kb(kb, model={}):
    for fact in kb.facts:
        if not evaluate_fact(fact, model):
            return False
    for sentence in kb.generic_sentences:
        if not evaluate_generic_sentences(sentence, model):
            return False

    return True


def truth_table_check_generickb(kb, query):
    entailed = True
    count = 0

    # Get all prop symbols from a KB
    symbols = kb.get_all_symbols()
    # print(symbols)

    # Generate all models
    models = generate_models(symbols)
    # print(models)
    print(len(models))
    for model in models:
        symbol_model = dict(zip(symbols, model))
        # print(symbol_model, evaluate_generic_kb(kb, symbol_model))
        if evaluate_generic_kb(kb, symbol_model):
            count += 1
            if not evaluate_generic_sentences(query, symbol_model):
                entailed = False

    return ("YES", count) if entailed else ("NO", count)
