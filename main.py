import sys
import re

from HornKB import *
from GenericKB import *
from truth_table import *
from forward_chaining import *
from backward_chaining import *
from resolution_prover import *

filename = sys.argv[1]
method = sys.argv[2]


def parse_input_file(input):
    content = input.split("ASK")
    tell_section = content[0].strip().replace(
        "TELL", "").strip()  # TELL section
    query = content[1].strip()  # Query

    horn_clause_pattern = r'\w+(\s*&\s*\w+)*\s*=>\s*\w+'
    generic_operator_pattern = r'[<=>|~()]'

    # Assume it's a Horn KB until proven otherwise
    is_horn = True

    # Check for the presence of generic sentences in tell_section
    sentences = tell_section.split(';')
    for sentence in sentences:
        sentence = sentence.strip()
        if re.search(generic_operator_pattern, sentence) and not re.match(horn_clause_pattern, sentence):
            is_horn = False
            break

    if re.search(generic_operator_pattern, query) and not re.match(horn_clause_pattern, query):
         is_horn = False

    if is_horn:
        kb = HornKB()
    else:
        kb = GenericKB()

    kb.parse_input(sentences, query)
    return kb


def main():
    # Read the input file
    with open(filename, 'r') as file:
        input_str = file.read()

    # Parse input to KB
    kb = parse_input_file(input_str)

    kb.display()

    if isinstance(kb, HornKB):
        if method == "FC":
            result, prop_list = fc_entails(kb, kb.query)
            if result:
                print("YES:", ", ".join(prop_list))
            else:
                print("NO")

        elif method == "BC":
            result, prop_list = bc_entails(kb, kb.query)
            if result:
                print("YES:", ", ".join(prop_list))
            else:
                print("NO")

        elif method == "TT":
            result, models_count = truth_table_check_hornkb(kb, kb.query)
            if result == "NO":
                print(result)
            else:
                print(result + ":", models_count)

        else:
            print("Invalid method!")
    else:
        if method == "TT":
            result, models_count = truth_table_check_generickb(kb, kb.query)
            if result == "NO":
                print(result)
            else:
                print(result + ":", models_count)
        elif method == "RES":
            result = res_entails(kb, kb.query)
            print(result)

        else:
            print("Invalid method!")


if __name__ == "__main__":
    main()
