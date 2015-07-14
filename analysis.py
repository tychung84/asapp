#loads library and dictionary
import json, re
import cPickle
import operator
lookupDict = cPickle.load(open('lookupDict.p'))
from flask import Flask, jsonify

def createDictionary(wordCount = 3, filename = 'lookupDict.p'):
    # initialized file load and removes most contractions. Ideally, I'd also run a spell check, but would need a 
    # list of names + unique places, so I forgo that process.
    k = json.load(open('sample_conversations.json'))
    allIssues = k['Issues']
    messageList = {}
    lookupDict = {}
    replaceDict = {"'m":' am', "'ve":' have', "'ll":" will", "'d":" would", "'s":" is", "'re":" are", "  ":" ", "' s": " is"}

    # removes all customer texts and only takes in a lower-case version of the customer interaction, saved into a dict
    for i in allIssues:
        for msg in i['Messages']:
            if not msg['IsFromCustomer']:
                smallMsg = re.findall(r"[\w' ]+", msg['Text'])

                for sMsg in smallMsg:
                    thisMessage = sMsg.strip().lower()

                    if len(thisMessage) > 1:
                        for item in replaceDict:
                            thisMessage = thisMessage.replace(item, replaceDict[item])

                        if thisMessage not in messageList.keys():
                            messageList[thisMessage] = 1
                        else:
                            messageList[thisMessage] += 1

    # uses the dictionary to create a master dictionary where the lookup will happen. The idea being that
    # over time, commonly used phrases will be counted more often.
    for keys in messageList:
        location = 0
        checker = 0
        
        for i in keys:
            if checker < 3:
                if i == ' ':
                    checker += 1
                location += 1

        for i in range(1, location):
            if keys[:i] not in lookupDict:
                lookupDict[keys[:i]] = {}
                lookupDict[keys[:i]][keys] = messageList[keys]
            elif keys not in lookupDict[keys[:i]]:
                lookupDict[keys[:i]][keys] = messageList[keys]

    # pickles the file 
    f = file(filename, 'wb')
    cPickle.dump(lookupDict, f)

def findPhrase(phrase):
    # finds the phrase by first checking how many words there are
        
    wordCount = phrase.count(' ')
    myPhrase = phrase.lower()
    
    # if there's only a few words, picks up the dictionary associate and sorts
    if wordCount <= 2:
        try:
            thisDict = lookupDict[myPhrase]
            sortedDict = sorted(thisDict.items(), key=operator.itemgetter(1), reverse=True)[:5]
            return [x.capitalize().replace(' i ', ' I ') for (x,y) in sortedDict]
        except KeyError:
            return []
    
    # otherwise, picks up the dictionary assorted and only picks out relevant data
    else:
        location = 0
        checker = 0
        
        for i in myPhrase:
            if checker < 3:
                if i == ' ':
                    checker += 1
                location += 1
        
        try:
            thisDict = lookupDict[myPhrase[:location - 1]]
            miniDict = {}
            
            for i in thisDict:
                if i[:len(myPhrase)] == myPhrase:
                    miniDict[i] = thisDict[i]
                    
            sortedDict = sorted(miniDict.items(), key=operator.itemgetter(1), reverse=True)[:5]
            return [x.capitalize().replace(' i ', ' I ') for (x,y) in sortedDict]
        except KeyError:
            return []

