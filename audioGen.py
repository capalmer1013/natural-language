"""
an attempt at using my NLP graph lib
to create .wav files using the same types of traversals
Currently it seems to make some pretty awesome crunchy
noises
"""
import wave
import graph

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
