from collections import defaultdict
from KB import *


def fc_entails(KB, query):

    # {clause: number of prop symbols in its premise}
    count = {clause: len(clause.premises) for clause in KB.clauses}

    # Prop symbols known to be true
    agenda = KB.facts

    # List of infered nodes (prop symbols), initially false
    inferred = defaultdict(bool)

    entailed_symbols = []
    entailed_symbols = (KB.facts)

    while agenda:
        p = agenda.pop()

        # If the query is a fact, return true
        if p == query:
            entailed_symbols.append(p)
            return True, entailed_symbols

        if not inferred[p]:
            inferred[p] = True
            entailed_symbols.append(p)

            # Decrease the count of clauses whose premises include p
            for clause in KB.clauses:
                if p in clause.premises:
                    count[clause] -= 1
                    # If all symbols in a clause is true, the conclusion is also true
                    if count[clause] == 0:
                        agenda.append(clause.conclusion)
    return False, entailed_symbols
