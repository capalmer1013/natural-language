import nltk
import re
from nltk.corpus import treebank
nltk.data.path.append('/run/media/cpalmer/WD/nltk_data')
pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)

prefixes = ['Mr.', 'Dr.', 'Ms.', 'Mrs.']
sentenceEnders = ['.', '?', '!']
with open('fear_and_loathing.txt', 'r') as f:
    text = ''
    for line in f:
        line = line.strip()
        text += line+' '

listOfSentences = pat.findall(text)

i = 0
for sentence in listOfSentences:
    if sentence in prefixes:
        listOfSentences[i] += listOfSentences[i+1]
        del listOfSentences[i+1]
    i += 1

listOfTokens = []
listOfTaggedTokens = []
for sentence in listOfSentences:
    listOfTokens.append(nltk.wordpunct_tokenize(sentence))

for token in listOfTokens:
    listOfTaggedTokens.append(nltk.pos_tag(token))
print 'hello'


# tokens = nltk.wordpunct_tokenize(text)
#
# tagged = nltk.pos_tag(tokens)
#
# text = nltk.Text(tokens)
