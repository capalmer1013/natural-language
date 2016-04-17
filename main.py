import nltk
import re
import objects
from nltk.corpus import treebank

G = objects.weightedGraph()

nltk.data.path.append('/run/media/cpalmer/WD/nltk_data')
pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)

prefixes = ['Mr.', 'Dr.', 'Ms.', 'Mrs.']
sentenceEnders = ['.', '?', '!']
with open('fl-clean.txt', 'r') as f:
    text = ''
    for line in f:
        line = ' '.join(line.split())
        line = line.strip()
        text += line+' '

listOfSentences = pat.findall(text)

i = 0
for sentence in listOfSentences:
    if sentence in prefixes:
        listOfSentences[i] += listOfSentences[i+1]
        del listOfSentences[i+1]
    i += 1

listOfWords = []
listOfTokens = []
listOfTaggedTokens = []
listOfSentenceTags = []
listOfTaggedWords = []

for sentence in listOfSentences:
    listOfTokens.append(nltk.wordpunct_tokenize(sentence))

for token in listOfTokens:
    listOfTaggedTokens.append(nltk.pos_tag(token))

# for token in listOfTokens:
#     for word in token:
#         if word not in listOfWords:
#             listOfWords.append(word)

for sentenceTag in listOfTaggedTokens:
    tempList = []
    for word in sentenceTag:
        if word not in listOfWords:
            listOfWords.append(word)

        tempList.append(word[1])
    if tempList not in listOfSentenceTags:
        listOfSentenceTags.append(tempList)

for sentence in listOfTokens:
    prevWord = ''
    for word in sentence:
        if word not in G.states:
            G.states.append(word)
        if prevWord == '':
            prevWord = word
            G.trainStart(word)
        else:
            G.train(prevWord, word)
            prevWord = word

for taggedTokens in listOfTaggedTokens:
    for token in taggedTokens:
        if token not in listOfTaggedWords:
            listOfTaggedWords.append(token)
for i in range(10):
    print G.generateSentence(listOfTaggedWords, listOfSentenceTags)
print 'hello'


# tokens = nltk.wordpunct_tokenize(text)
#
# tagged = nltk.pos_tag(tokens)
#
# text = nltk.Text(tokens)
