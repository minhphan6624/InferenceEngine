import sys

from KB import *
from truth_table import *
from forward_chaining import *
from backward_chaining import *

filename = sys.argv[1]
# method = sys.argv[2]


def test_truth_table():
    # Create a KB and query
    kb = KB()
    kb.clauses = [HornClause("p&q=>r"), HornClause("r=>s")]
    kb.facts = ['p', 'q']
    query = 's'

    # Use the truth table check function
    result = truth_table_check(kb, query)
    # assert result == ("YES", ), "Test failed: Query should be entailed by the KB"

    print(result)


def main():
    # # Initialize a new KB
    main_KB = KB()

    # Parse input file
    # main_KB.parse_input_file(filename)

    # result = truth_table_check(main_KB, main_KB.query)

    # print(result)

    # Display for debugging purposes
    # main_KB.display()

    # if method == TT:
    #     pass

    test_truth_table()


if __name__ == "__main__":
    main()
