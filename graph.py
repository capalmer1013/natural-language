""" Module Docstring because PyLint
    Graphs are in the form
    G[node][edge] = weight
    G = {
        node: {
            edge: weight
        }
    }
"""
import re
import string
import json
import random

# TODO generalize this to use any hashable thing as a node

def addLineToWeightedGraph(G, L):
    """ given a line of text and a graph:
        This function is intended to append the
        probability of word traversals to the graph
    """
    PrevState = ''
    L = L.split()
    for each in L:
        # removes non-printable characters
        each = ''.join([x for x in each if x in string.ascii_letters])

        if not PrevState:
            PrevState = each
            continue

        if PrevState not in G:
            G[PrevState] = {}

        if each not in G[PrevState]:
            G[PrevState][each] = 0

        G[PrevState][each] += 1
        PrevState = each


def traverseGraph(G, n, node=None):
    """ Generate a traversal of length n
    """
    traversal = []
    if not node:
        node = random.choice(G.keys())

    for _ in range(n):
        traversal.append(node)
        #print traversal
        den = sum([G[node][x] for x in G[node]])
        choices = [(c, float(G[node][c])/den) for c in G[node]]
        node = weighted_choice(choices)

    return traversal


def weighted_choice(choices):
    """ Helper function
        used to make weighted choice for traversal
    """
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def saveGraph(G, filename):
    """ Saves graph in json format
    """
    # TODO make all file file accessing done with context manager
    outfile = open(filename, 'w')
    outfile.write(json.dumps(G, indent=4, sort_keys=True))
    # json.dump(graph, outfile)  # this one looks gross


def openGraph(filename):
    """ Open a json formatted graph in dict form
    """
    f = open(filename)
    G = json.load(f)
    f.close()
    return G


def testMakingFile():
    """ just to test if things work the way I think they should
    """
    filename = "fear_and_loathing.txt"
    f = open(filename)
    graph = {}
    lines = [i for i in f if re.search("[a-zA-Z]", i)]  # if there are characters in line

    f.close()
    wholeThing = "".join(lines)

    addLineToWeightedGraph(graph, wholeThing)

    #for line in lines:
    #    addLineToWeightedGraph(graph, line)

    saveGraph(graph, "wordGraph.json")


def testOpeningAndGenerating():
    """ test opening an already saved file
    """
    graph = openGraph("wordGraph.json")
    print ' '.join(traverseGraph(graph, 20))


if __name__ == "__main__":
    testMakingFile()
    testOpeningAndGenerating()
