# web/app/food_reviews/sentence_generation.py

""" Setence Generaion Docstring

This module is to return lists of strings as sentences generated from t-
ri-gram model using Amazon Reviews dataset. There're two types of gener-
ated sentences based on the dataset: "sentences from helpful reviews" a-
nd "sentences from non-helpful reviews".

Example:

Attributes:

Todo:

"""

# from json import dumps
from app.utilities import load_zip_data

def recursion(sent, sents, trigrams):

    """
    recursion

    Function to extract list of strings using recursion

    Args: 
        sent (List)
        sents (List)
        trigrams (dict)

    Returns: 
        sents (List)

    """

    w1, w2 = sent[-2:]

    # terminating condition: end of sentence or sentence length
    if (w1 == '</s>') | (w2 == '</s>'): 
        sents.append(sent[2:-1]) # remove <s> and </s>
        return sents
    if len(sent) >= 15: # limit setence length
        return sents
    
    # iterate each word on subset 
    for word in trigrams[w1][w2].keys():
        sents = recursion(sent+[word], sents, trigrams)

    return sents


def genereate_sentences(zipPath, fileName, first_word='i'):

    """
    genereate_sentences

    Function to return lists of generated sentences with recursion

    Args: 
        first_word (str)

    Returns: 
        sentences (dict)

    """

    data = load_zip_data(zipPath, fileName)

    helpful_sentences = recursion(
        ['<s>', '<s>', first_word], [], data['helpful']
    )
    not_helpful_sentences = recursion(
        ['<s>', '<s>', first_word], [], data['notHelpful']
    )

    sentences = {
        'helpful': helpful_sentences, 
        'notHelpful': not_helpful_sentences
        }

    return sentences
