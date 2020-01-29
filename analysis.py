import re
from collections import Counter, namedtuple, defaultdict
from string import punctuation, whitespace
from newspaper import Article
import nltk
from nltk.corpus import stopwords

import spacy
from spacy import displacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")
stop_words = stopwords.words("english")

def get_names(text):
    doc = nlp(text)
    entities = [(X.text, X.label_) for X in doc.ents]

    names = []
    for entity in entities:
        if entity[1] == 'PERSON' or entity[1] == "GPE" or entity[1] == "ORG":
            names.append(entity[0])

    return names

def to_lower(text):
    return text.lower()

def strip_numbers(content):
    return ''.join(c for c in content if not c.isdigit())

def extract_keywords(url):
    '''
    Input: HTTP URL
    Ouput: List of keywords compiled from names found in the article title and keywords found in the article text
    '''
    a = Article(url)
    a.download()
    a.parse()
    a.nlp()
    keywords = a.keywords
    title = a.title
    content = a.text

    #clean up content
    content = to_lower(content)
    content = strip_numbers(content)

    #clean up title
    title = to_lower(title)
    title = strip_numbers(title)

    #get names and identities from content text
    content_names = get_names(''.join(content))

    top_keywords = []
    for name in content_names:
        if name in title:
            #if the name is in the title, it is significant
            top_keywords.append(name)

    for keyword in keywords:
        if keyword in title and keyword not in stop_words and not keyword.isdigit():
            #Find other keywords that are not names and are found in the title
            top_keywords.append(keyword)

    if not top_keywords:
        top_keywords = title.split(" ")

    #remove duplicates
    top_keywords = list(dict.fromkeys(top_keywords))

    return top_keywords, a.title