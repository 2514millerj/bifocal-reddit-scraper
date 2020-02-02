import re
from collections import Counter, namedtuple, defaultdict
from string import punctuation, whitespace
from newspaper import Article, Config
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import logging

import spacy
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

def get_thumbnail_image(html):
    soup = BeautifulSoup(html)
    thumbnail = soup.find("meta",  property="og:image", features="lxml")

    if thumbnail:
        return thumbnail["content"]
    else:
        return ''

def to_lower(text):
    return text.lower()

def strip_numbers(content):
    return ''.join(c for c in content if not c.isdigit())

def parse_submission(url):
    '''
    Input: HTTP URL
    Ouput: List of keywords compiled from names found in the article title and keywords found in the article text
    '''
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent

    a = Article(url, config=config)
    try:
        a.download()
        a.parse()
    except Exception as e:
        logging.error(e)
        return

    a.nlp()
    keywords = a.keywords
    title = a.title
    content = a.text
    thumbnail_image = get_thumbnail_image(a.html)

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

    return {'keywords': top_keywords, 'title': a.title, 'thumbnail_url': thumbnail_image}