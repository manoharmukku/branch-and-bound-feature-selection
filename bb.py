# Author: Manohar Mukku
# Date: 15.09.2018
# Desc: Branch and Bound implementation for feature selection
# Github: https://github.com/manoharmukku/branch-and-bound-feature-selection

import getopt
import sys

def usage():
    return None

def parse_features(features_string):
    return list(map(int, features_string.split(', ')))

def main(argv):
    # Get the command line arguments
    try:
        opts, args = getopt.getopt(argv, "hf:", ["help", "features="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    features = [1, 2, 3, 4, 5]
    for opt, arg in opts:
        if (opt in ["-h", "--help"]):
            usage()
            sys.exit()
        elif (opt in ["-f", "--features"]):
            features = parse_features(arg)

if __name__ == "__main__":
    main(sys.argv[1:])