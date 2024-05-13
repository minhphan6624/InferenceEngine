from collections import defaultdict
from KB import *

def bc_entails(KB, query):

    # {clause: number of prop symbols in its premise}
    count = {clause : len(clause.premises) for clause in KB.clauses}

    # Prop symbols known to be true
    agenda = [query]

    #List of infered nodes (prop symbols), initially false
    inferred = defaultdict(bool)

    while agenda:
        p = agenda.pop()

        
    return False