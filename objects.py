class weightedGraph:
    def __init__(self):
        self.states = ['<begin>']
        self.edges = {'<begin>': []}
        # edges
        # {fromState: [{weight: rational, data: toState}] }

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

                i = self.edges[fromState].find(toState)
                self.edges[fromState][i].numerator += 1

                for outState in self.edges[fromState]:
                    outState['weight'].denominator += 1

            else:

                self.edges[fromState].append({'weight': rational(), 'data': toState})
                self.edges[fromState][-1]['weight'].numerator += 1

                for outState in self.edges[fromState]:
                    outState['weight'].denominator += 1

        else:
            self.edges[fromState] = [{'weight': rational(), 'data': toState}]

            for item in self.edges[fromState]:
                item['weight'].numerator += 1
                item['weight'].denominator += 1


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