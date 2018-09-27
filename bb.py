# Author: Manohar Mukku
# Date: 15.09.2018
# Desc: Branch and Bound implementation for feature selection
# Github: https://github.com/manoharmukku/branch-and-bound-feature-selection

import getopt
import sys
import random
from graphviz import Digraph
import queue
import itertools

def criterion_function(features):
    return sum(features)

    '''
    # Squared criterion function
    result = 0
    for feat in features:
        result += feat**2
    return result
    '''
    
def isMonotonic(features):
    features = sorted(features)

    # Generate the powerset of the features
    powerset = []
    for i in range(1, len(features)+1):
        subset = itertools.combinations(features, i)
        powerset.extend(subset)

    # For all possible subset pairs, check if monotonicity is satisfied
    # print (powerset)
    for i, item1 in enumerate(powerset):
        for item2 in powerset[i+1:]:
            if (set(item1).issubset(set(item2)) and (criterion_function(list(item1)) > criterion_function(list(item2)))):
                return False

    return True

class tree_node(object):
    def __init__(self, value, features, preserved_features, level):
        self.branch_value = value
        self.features = features
        self.preserved_features = preserved_features
        self.level = level
        self.index = None
        self.children = []
        self.J = None

flag = True
J_max = -1
result_node = None

def branch_and_bound(root, D, d):
    global flag
    global J_max
    global result_node

    # Compute the criterion function
    root.J = criterion_function(root.features)

    # Stop building children for this node, if J <= J_max
    if (flag == False and root.J <= J_max):
        return

    # If this is the leaf node, update J_max, result_node and return
    if (root.level == D-d):
        if (flag == True):
            J_max = root.J
            flag = False
            result_node = root

        elif (root.J > J_max):
            J_max = root.J
            result_node = root

        return

    # Compute the number of branches for this node
    no_of_branches = (d + 1) - len(root.preserved_features)

    # Generate the branches
    branch_feature_values = sorted(random.sample(list(set(root.features)-set(root.preserved_features)), no_of_branches))

    # Iterate on the branches, and for each branch, call branch_and_bound recursively
    for i, branch_value in enumerate(branch_feature_values):
        child = tree_node(branch_value, [value for value in root.features if value != branch_value], \
            root.preserved_features + branch_feature_values[i+1:], root.level+1)

        root.children.append(child)

        branch_and_bound(child, D, d)

def give_indexes(root):
    bfs = queue.Queue(maxsize=40)

    bfs.put(root)
    index = -1
    while (bfs.empty() == False):
        node = bfs.get()
        node.index = index
        index += 1
        for child in node.children:
            bfs.put(child)

def display_tree(node, dot_object, parent_index):
    # Create node in dob_object, for this node
    dot_object.node(str(node.index), "Features = " + str(node.features) + "\nJ(Features) = " + str(node.J) + "\nPreserved = " + str(node.preserved_features))

    # If this is not the root node, create an edge to its parent
    if (node.index != -1):
        dot_object.edge(str(parent_index), str(node.index), label=str(node.branch_value))

    # Base case, when the node has no children, return
    if (len(node.children) == 0):
        return

    # Recursively call display_tree for all the childern of this node
    for child in reversed(node.children):
        display_tree(child, dot_object, node.index)

def usage():
    print ("------------------------------------------------------------------------------------")
    print ("usage: bb.py [-h | --help] [-d | --defaults] -f | --features ... -p | --preserve ...")
    print ("------------------------------------------------------------------------------------")
    print ("Ex: $ python bb.py -f 1,2,3,4,5 -d 2")
    print ("-h or --help      --> optional, used to display help")
    print ("-d or --defaults  --> optional/required, used to specify the use of default values for unspeceified arguments. Optional when all the arguments are specified")
    print ("-f or --features= --> required, used to specity feature values, comma-separated without spaces (Ex: -f 1,2,3,4,5)")
    print ("-p or --preserve= --> required, used to specify the number of features to select (Ex: -p 2)")
    return

def parse_features(features_string):
    return sorted([float(str) for str in features_string.split(',')])

def main(argv):
    # Get the command line arguments
    try:
        opts, args = getopt.getopt(argv, "hdf:p:", ["help", "defaults", "features=", "preserve="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Defaults
    features = None
    D = None
    d = None
    defaults = False
    flag = 0

    # Parse the command line arguments
    for opt, arg in opts:
        if (opt in ["-h", "--help"]):
            usage()
            sys.exit()
        elif (opt in ["-d", "--defaults"]):
            defaults = True
            print ("Using default values for unspecified arguments")
        elif (opt in ["-f", "--features"]):
            features = arg
            flag |= 1 # Set 1st bit from last to 1
        elif (opt in ["-p", "--preserve"]):
            d = arg
            flag |= 2 # Set 2nd bit from last to 1

    # Sanity check of command line arguments
    if (defaults == False and flag != 3): # If neither all the required features are specified, nor the default flag is set
        sys.exit("Oops! Please specify all the required arguments, or run the program with -d or --defaults flag (-h for help)")

    if (defaults == True):
        if (features == None):
            features = "1,2,3,4,5"
        if (d == None):
            d = "2"

    try:
        features = parse_features(features)
        D = len(features)
    except ValueError:
        sys.exit("Oops! The feature values should be numeric")

    try:
        int(d)
    except ValueError:
        sys.exit("Oops! Number of features to select, p, should be an integer value")
    d = int(d)

    if (d <= 0):
        sys.exit("Oops! Desired number of features value should be > 0")
    if (d > D):
        sys.exit("Oops! Desired number of features value should be atmost the number of features supplied ({})".format(D))

    # Check monotonicity of J
    if (isMonotonic(features) == False):
        sys.exit("Oops! The feature values do not satisfy monotonic increasing")

    # Create the root tree node
    root = tree_node(-1, features, [], 0)

    # Call branch and bound on the root node, and recursively construct the tree
    branch_and_bound(root, D, d)

    # Give indexes(numbers) for nodes of constructed tree in BFS order (used for Graphviz)
    give_indexes(root)

    # Display the constructed tree using python graphviz
    print ("Plotting branch and bound tree...")
    dot = Digraph(comment="Branch and Bound Feature selection")
    dot.format = "png"
    display_tree(root, dot, -1)
    dot.render("bb_tree", view=True)
    print ("Plotting finished...")

    # Print the result
    print ("------")
    print ("Output")
    print ("------")
    print ("Features considered = {}".format(result_node.features))
    print ("Criteriion function value = {}".format(result_node.J))

if __name__ == "__main__":
    main(sys.argv[1:])
