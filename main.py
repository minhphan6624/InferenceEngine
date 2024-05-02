import sys
from KB import *

filename = sys.argv[1]
#method = sys.argv[2]

def parse_input_file(filename):
    with open(filename, "r") as f:
        f.readline() #First line only contains "TELL"
        tell_sentences = f.readline().strip().split(";")

        for sentence in tell_sentences:
            sentence = sentence.replace(" ", "'") #Remove space inside a sentence
            if (sentence.find("=>")):
                


def main():
    pass


if __name__ == "__main__":
    main()
