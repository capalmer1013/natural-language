import random


class weightedGraph:
    def __init__(self):
        self.states = ['<begin>']
        self.edges = {'<begin>': []}
        # edges
        # {fromState: [{weight: rational, data: toState}] }

    def rebalanceEdges(self, listOfEdges):
        denominatorCount = 0
        for edge in listOfEdges:
            denominatorCount += edge['weight'].numerator

        for edge in listOfEdges:
            edge['weight'].denominator = denominatorCount

    def trainStart(self, toState):
        found = False

        for each in self.edges['<begin>']:
            if each['data'] == toState:
                each['weight'].numerator += 1
                found = True

        if not found:
            self.edges['<begin>'].append({'weight': rational(), 'data': toState})
            self.edges['<begin>'][-1]['weight'].numerator += 1
            self.edges['<begin>'][-1]['weight'].denominator += 1

        else:
            for each in self.edges['<begin>']:
                each['weight'].denominator += 1

    def train(self, fromState, toState):
        if fromState in self.edges:
            if toState in self.edges[fromState]:

                i = self.edges[fromState].index(toState)
                self.edges[fromState][i].numerator += 1

                self.rebalanceEdges(self.edges[fromState])

            else:

                self.edges[fromState].append({'weight': rational(), 'data': toState})
                self.edges[fromState][-1]['weight'].numerator += 1

                self.rebalanceEdges(self.edges[fromState])

        else:
            self.edges[fromState] = [{'weight': rational(), 'data': toState}]

            for item in self.edges[fromState]:
                item['weight'].numerator += 1

            self.rebalanceEdges(self.edges[fromState])

    def generateSentence(self, listOfTaggedWords, listOfTaggedSentences):
        returnString = ''
        sentenceList =[]
        tagList = []
        done = False
        nextState = self.findNextState('<begin>')
        if nextState is None:
            done = True

        listOfPossibleSentenceStructs = listOfTaggedSentences

        while not done:
            index = 0
            returnString += nextState + ' '
            sentenceList.append(nextState)
            for taggedWord in listOfTaggedWords:
                if taggedWord[0] == nextState:
                    index = listOfTaggedWords.index(taggedWord)

            tagList.append(listOfTaggedWords[index])

            try:
                tempState = self.findNextState(nextState)
            except KeyError:
                return returnString

            possibleNextTag = []
            foundInNextPossibleTag = False
            while not foundInNextPossibleTag and len(possibleNextTag) > 0:
                try:
                    tempState = self.findNextState(nextState)
                except KeyError:
                    return returnString
                for taggedWord in listOfTaggedWords:
                    if taggedWord[0] == tempState:
                        foundInNextPossibleTag = True

            nextState = tempState
            if nextState is None:
                done = True

            for sentenceStructure in listOfPossibleSentenceStructs:
                if sentenceStructure[:len(tagList)] != tagList:
                    del listOfPossibleSentenceStructs[listOfPossibleSentenceStructs.index(sentenceStructure)]

            for sentenceStructure in listOfPossibleSentenceStructs:
                try:
                    if sentenceStructure[len(tagList)] not in possibleNextTag:
                        possibleNextTag.append(sentenceStructure[len(tagList)])
                except IndexError:
                    return returnString

            if tagList in listOfTaggedSentences:
                done = True

        return returnString

        print 'balls'

    def findNextState(self, currentState):
        randomFloat = random.random()
        for i in self.edges[currentState]:
            if i['weight'].toFloat() > 0:
                if i['weight'].toFloat() > randomFloat:
                    return i['data']
                else:
                    randomFloat = randomFloat - i['weight'].toFloat()

class rational:
    def __init__(self):
        self.numerator = 0
        self.denominator = 0

    def toString(self):
        return str(self.toFloat())

    def toFloat(self):
        return float(self.numerator)/float(self.denominator)

    def fromString(self, thisString):
        index = thisString.find('/')
        self.numerator = thisString[:index]
        self.denominator = thisString[index+1:]