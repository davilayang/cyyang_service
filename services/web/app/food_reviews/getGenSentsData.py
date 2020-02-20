from flask import url_for
import json
import zipfile

# filePath = url_for('static', filename='data/helpful_reviews.zip' )
filePath = 'app/static/data/helpful_reviews.zip'
with zipfile.ZipFile(filePath) as zfile:
    data = json.loads(zfile.read('helpful_reviews.json').decode("utf-8"))

def getAvailableWords():
    helpfulFirst =  list(data['helpful']['<s>']['<s>'].keys())
    notHelpfulFirst =  list(data['notHelpful']['<s>']['<s>'].keys())

    return {'helpful': helpfulFirst, 'notHelpful': notHelpfulFirst}

def getGenSents(firstWord='i'):

    def recursion(sent, sents, trigrams):
        w1, w2 = sent[-2:]
        # terminate condition: end of sentence or sentence length
        if (w1 == '</s>') | (w2 == '</s>'): 
            sents.append(sent[2:-1]) # remove <s> and </s>
            return sents
        if len(sent) >= 15: # limit setence length
            return sents
        
        # iterate each word on subset 
        for word in trigrams[w1][w2].keys():
            sents = recursion(sent+[word], sents, trigrams)
        return sents

    helpfulSents = recursion(['<s>', '<s>', firstWord], [], data['helpful'])
    notHelpfulSents = recursion(['<s>', '<s>', firstWord], [], data['notHelpful'])

    return json.dumps({'helpful': helpfulSents, 'notHelpful': notHelpfulSents})

