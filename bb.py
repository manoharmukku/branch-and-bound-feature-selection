# Author: Manohar Mukku
# Date: 15.09.2018
# Desc: Branch and Bound implementation for feature selection
# Github: https://github.com/manoharmukku/branch-and-bound-feature-selection

import getopt
import sys

def usage():
    return None

def main(argv):
    # Get the command line arguments
    try:
        opts, args = getopt.getopt(argv, "hf:", ["help", "features="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if (opt in ["-h", "--help"]):
            usage()
            sys.exit()
        elif (opt in ["-f", "--features"]):
            features = arg

if __name__ == "__main__":
    main(sys.argv[1:])