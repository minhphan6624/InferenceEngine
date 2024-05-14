import sys

from KB import *
from truth_table import *
from forward_chaining import *
from backward_chaining import *

filename = sys.argv[1]
method = sys.argv[2]

def main():
    #Initialize KB
    main_KB = KB()

    # Parse input file
    main_KB.parse_input_file(filename)


    if method == "FC":
        result, prop_list = fc_entails(main_KB, main_KB.query)
        if result:
            print("YES:" , ", ".join(prop_list))
        else:
            print("NO")

    elif method == "BC":
        result, prop_list = bc_entails(main_KB, main_KB.query)
        if result:
            print("YES:" , ", ".join(prop_list))
        else:
            print("NO")

    elif method == "TT":
        result, models_count = truth_table_check(main_KB, main_KB.query)
        print(result + ":", models_count)

    else:
        print("Invalid method!")


if __name__ == "__main__":
    main()
