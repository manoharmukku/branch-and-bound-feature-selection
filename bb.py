# Author: Manohar Mukku
# Date: 15.09.2018
# Desc: Branch and Bound implementation for feature selection
# Github: https://github.com/manoharmukku/branch-and-bound-feature-selection

import getopt
import sys
import random

def criterion_function(features):
    return sum(features)

class tree_node(object):
    def __init__(self, value, features, preserved_features, level):
        self.branch_value = value
        self.features = features
        self.preserved_features = preserved_features
        self.level = level
        self.children = []
        self.J = None

flag = True

def branch_and_bound(root, D, d, J_max):
    # Compute the criterion function
    root.J = criterion_function(root.features)

    # Stop building children for this node, if J <= J_max
    if (!flag && root.J <= root.J_max):
        return None

    # If this is the leaf node, update J_max and return
    if (root.level == D-d):
        if (flag == True):
            J_max = root.J
            flag = False
        elif (root.J > J_max):
            J_max = root.J

        return None

    # Compute the number of branches
    no_of_branches = (d + 1) - len(root.preserved_features)

    # Generate the branches
    branch_feature_values = sorted(random.sample(list(set(root.features)-set(root.preserved_features)), no_of_branches))

    # Iterate on the branches, and for each branch call branch_and_bound recursively
    for index, value in enumerate(branch_feature_values):
        child = tree_node(value, [n for n in root.features if n != value] , root.preserved_features + branch_feature_values[(index+1):], root.level+1)

        root.children.append(child)

        branch_and_bound(child, D, d, J_max)


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

    # Create the root tree node


if __name__ == "__main__":
    main(sys.argv[1:])