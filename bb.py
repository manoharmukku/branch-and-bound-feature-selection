# Author: Manohar Mukku
# Date: 15.09.2018
# Desc: Branch and Bound implementation for feature selection
# Github: https://github.com/manoharmukku/branch-and-bound-feature-selection

import getopt
import sys
import random
from graphviz import Digraph

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
    global flag

    # Compute the criterion function
    root.J = criterion_function(root.features)

    # Stop building children for this node, if J <= J_max
    if (flag == False and root.J <= J_max):
        return

    # If this is the leaf node, update J_max and return
    if (root.level == D-d):
        if (flag == True):
            J_max = root.J
            flag = False
        elif (root.J > J_max):
            J_max = root.J

        return

    # Compute the number of branches
    no_of_branches = (d + 1) - len(root.preserved_features)

    # Generate the branches
    branch_feature_values = sorted(random.sample(list(set(root.features)-set(root.preserved_features)), no_of_branches))

    # Iterate on the branches, and for each branch call branch_and_bound recursively
    for index, value in enumerate(branch_feature_values):
        child = tree_node(value, [n for n in root.features if n != value] , root.preserved_features + branch_feature_values[(index+1):], root.level+1)

        root.children.append(child)

        branch_and_bound(child, D, d, J_max)

index = 0

def display_tree(node, dot_object, node_index, parent_index):
    global index

    # Create node in dob_object, for this node
    dot_object.node(str(node_index), "Features = " + str(node.features) + "\nPreserved = " + str(node.preserved_features) + "\nJ = " + str(node.J))

    # If this is not the root node, create an edge to its parent
    if (node_index != -1):
        dot_object.edge(str(parent_index), str(node_index), label=str(node.branch_value))

    # Base case, when the node has no children, return
    if (len(node.children) == 0):
        return

    # Recursively call display_tree for all the childern of this node
    for child in reversed(node.children):
        display_tree(child, dot_object, index, node_index)
        index += 1

def usage():
    return

def parse_features(features_string):
    return list(map(int, features_string.split(', ')))

def main(argv):
    # Get the command line arguments
    try:
        opts, args = getopt.getopt(argv, "hf:d", ["help", "features=", "desired"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    features = [1, 2, 3, 4, 5]
    D = 5
    d = 2
    for opt, arg in opts:
        if (opt in ["-h", "--help"]):
            usage()
            sys.exit()
        elif (opt in ["-f", "--features"]):
            features = parse_features(arg)
            D = len(features)
        elif (opt in ["-p", "--desired"]):
            d = int(arg)

    # Create the root tree node
    root = tree_node(-1, features, [], 0)

    # Call branch and bound on the root node, and construct the tree
    branch_and_bound(root, D, d, -1)

    # Display the constructed tree using python graphviz
    dot = Digraph(comment="Branch and Bound Feature selection")
    dot.format = "png"
    display_tree(root, dot, -1, -1)
    dot.render("bb_tree", view=True)

if __name__ == "__main__":
    main(sys.argv[1:])