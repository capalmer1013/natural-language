import nltk
import re
import objects
# from twitter import *
import twitter
from nltk.corpus import treebank

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

print 'authorizing'
# api = twitter.Api(consumer_key='x5bCSpVNRktPA8I77CEuiXBAF', consumer_secret='j3y323NvjALJk8JwmoMYQtKKr4nUrCGHQgnjxecI51wduofPeS',
#                   access_token_key='721754140406374400-ONJDR3cBSX5Xy1UBtZxZ5HTNRgB0lfw',
#                   access_token_secret='ht3AeapviyiQ7whquilPv5pKNbmMLul6nsBqeTUmuedt4')

api = twitter.Api(consumer_key='sKv44OsnEe7IjYBihLANYRJqd', consumer_secret='JnQld76SytuXVi0FuKhCmM8G2GeziiZMta0ffR5EpWblsLRssM',
                  access_token_key='707825255121821697-O8PIQ7F0yAYWpT2do56xxUbtWNVRK4c',
                  access_token_secret='oSIEKyc70gi0g5NYCMm8XBZdN6SF6D643Z6dQggTqnkYy')

print 'getting friends'
users = api.GetFriends()
statuses = []
print 'getting statuses'
for u in users:
    timeline = api.GetUserTimeline(u)
    for each in timeline:
        statuses.append(each.text)

# token =
# token_key =
# con_secret =  vY53NMXFGB4HMycdQtusJrlo
# con_secret_key =
# t = Twitter(
#     auth=OAuth(token, token_key, con_secret, con_secret_key)
# )
print 'good to go'
G = objects.weightedGraph()

nltk.data.path.append('/run/media/cpalmer/WD/nltk_data')
pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)

# prefixes = ['Mr.', 'Dr.', 'Ms.', 'Mrs.']
# sentenceEnders = ['.', '?', '!']
# with open('fl-clean.txt', 'r') as f:
#     text = ''
#     for line in f:
#         line = ' '.join(line.split())
#         line = line.strip()
#         text += line+' '

# listOfSentences = pat.findall(text)
listOfSentences = []
for status in statuses:
    if '@' not in status:
        listOfSentences.append(status)
#listOfSentences = statuses

# i = 0
# for sentence in listOfSentences:
#     if sentence in prefixes:
#         listOfSentences[i] += listOfSentences[i+1]
#         del listOfSentences[i+1]
#     i += 1

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

tweet = G.generateSentence(listOfTaggedWords, listOfSentenceTags)
listofAts = find(tweet, '@')
for index in listofAts:
    tweet = tweet[:index]+tweet[index+1:]

if len(tweet) > 140:
    tweet = tweet[:140]

api.PostUpdate(tweet)
    # print G.generateSentence(listOfTaggedWords, listOfSentenceTags)
print 'hello'


# tokens = nltk.wordpunct_tokenize(text)
#
# tagged = nltk.pos_tag(tokens)
#
# text = nltk.Text(tokens)
