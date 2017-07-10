"""
an attempt at using my NLP graph lib
to create .wav files using the same types of traversals
Currently it seems to make some pretty awesome crunchy
noises
"""
import wave
import graph

import struct
from mpl_toolkits.axes_grid.axislines import SubplotZero
import matplotlib.pyplot as plt
import numpy as np

# Something important to remember:
# 8bit wavs are unsigned
# 16bit wavs are signed.
# will need to add flexibility for this

def graphWaveSamples(samples):
    y = [struct.unpack('h', i)[0] for i in samples]
    #print y
    print "max:", max(y)
    print "min:", min(y)
    print "avg:", sum(y)/float(len(y))
    fig = plt.figure(1)
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)

    for direction in ["xzero", "yzero"]:
        ax.axis[direction].set_axisline_style("-|>")
        ax.axis[direction].set_visible(True)

    for direction in ["left", "right", "bottom", "top"]:
        ax.axis[direction].set_visible(False)

    x = range(len(y))
    ax.plot(x, y)

    plt.show()


def findCyclePeriods(samples):
    samples = [struct.unpack('h', i)[0] for i in samples]  # turn samples into signed ints
    previous = None
    cycleBeginings = []
    count = -1

    for sample in samples:
        count += 1
        if not previous:
            previous = sample
            continue
        
        if previous <= 0 and sample >= 0:
            cycleBeginings.append(count)
    
        previous = sample

    return cycleBeginings


infileName = 'sample.wav'
outfileName = 'new.wav'

frames = []
G = {}

a = wave.open(infileName, 'r')
b = wave.open(outfileName, 'w')

sampleWidth = a.getsampwidth()

b.setnchannels(1)
b.setsampwidth(a.getsampwidth())
b.setframerate(a.getframerate())

for _ in range(a.getnframes()):
    frames.append(a.readframes(1)[:sampleWidth])

sentence = ' '.join(frames)
graph.createWeightedGraphFromSequence(G, sentence)

newTraversal = []
for _ in range(10):
    newTraversal.extend(graph.traverseGraph(G, len(frames)))

b.writeframes(''.join(newTraversal))
b.close()

graphWaveSamples(frames)
