import sys

from KB import *
from truth_table import *
from forward_chaining import *
from backward_chaining import *

filename = sys.argv[1]
method = sys.argv[2]


def test_truth_table():
    # Create a KB and query
    kb = KB()
    kb.clauses = [HornClause("p&q=>r"), HornClause("r=>s")]
    kb.facts = ['p', 'q']
    query = 's'

    # Use the truth table check function
    # result = truth_table_check(kb, query)
    result = fc_entails(kb, query)

    # assert result == ("YES", ), "Test failed: Query should be entailed by the KB"

    print(result)


def main():
    main_KB = KB()

    # Parse input file
    main_KB.parse_input_file(filename)

    main_KB.display()

    if method == "FC":
        result = fc_entails(main_KB, main_KB.query)
    elif method == "BC":
        result = bc_entails(main_KB, main_KB.query)
    elif method == "TT":
        result = "Not implemented"
    else:
        result = "Invalid method!"

    print(result)
    # Display for debugging purposes


if __name__ == "__main__":
    main()
