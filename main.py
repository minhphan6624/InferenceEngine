import sys

from KB import *
from truth_table import *
from forward_chaining import *
from backward_chaining import *

filename = sys.argv[1]
method = sys.argv[2]


def test_truth_table():
    kb = KB()
    kb.clauses = [HornClause("p&q=>r"), HornClause("r=>s")]
    kb.facts = ['p', 'q']
    query = 's'

    result = truth_table_check(kb, query)
    # result = fc_entails(kb, query)

    print(result)


def main():
    main_KB = KB()

    # Parse input file
    main_KB.parse_input_file(filename)

    # main_KB.display()

    if method == "FC":
        result = fc_entails(main_KB, main_KB.query)
    elif method == "BC":
        result = bc_entails(main_KB, main_KB.query)
    elif method == "TT":
        result = test_truth_table()
    else:
        result = "Invalid method!"

    print(result)


if __name__ == "__main__":
    main()
