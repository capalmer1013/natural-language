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

testFilename = "fear_and_loathing.txt"
graphFile = "wordGraph.json"

def createWeightedGraphFromSequence(G, L):
    """ given a line of text and a graph:
        This function is intended to append the
        probability of word traversals to the graph
    """
    PrevState = '<START>'
    L = L.split()
    L.append("<END>")
    for each in L:
        # removes non-printable characters
        if not(each == "<START>" or each == "<END>"):
            each = ''.join([x for x in each if x in string.ascii_letters])

        if not each:
            continue

        if not PrevState:
            PrevState = each
            continue

        if PrevState not in G:
            G[PrevState] = {}

        if each not in G[PrevState]:
            G[PrevState][each] = 0

        G[PrevState][each] += 1
        PrevState = each



def traverseGraph(G, n, node="<START>"):
    """ Generate a traversal of length n
    """
    traversal = []
    if not node:
        node = random.choice(G.keys())

    while node != "<END>":
        den = sum([G[node][x] for x in G[node]])
        choices = [(c, float(G[node][c])/den) for c in G[node]]
        node = weighted_choice(choices)
        traversal.append(node)

    return traversal[:-1]


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
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(G, indent=4, sort_keys=True))


def openGraph(filename):
    """ Open a json formatted graph in dict form
    """
    with open(filename) as f:
        return json.load(f)


def testMakingFile():
    """ just to test if things work the way I think they should
    """
    with open(testFilename) as f:
        graph = {}
        lines = [i for i in f if re.search("[a-zA-Z]", i)]  # if there are characters in line

    for each in lines:
        createWeightedGraphFromSequence(graph, each)
    saveGraph(graph, graphFile)


def testOpeningAndGenerating():
    """ test opening an already saved file
    """
    graph = openGraph(graphFile)
    print ' '.join(traverseGraph(graph, 20))


if __name__ == "__main__":
    testMakingFile()
    testOpeningAndGenerating()
