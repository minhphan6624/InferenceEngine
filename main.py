import sys
from KB import *

filename = sys.argv[1]
# method = sys.argv[2]


def main():
    # Initialize a new KB
    main_KB = KB()

    main_KB.parse_input_file(filename)

    main_KB.display()


if __name__ == "__main__":
    main()
