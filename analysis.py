import re
from collections import Counter, namedtuple, defaultdict
from string import punctuation, whitespace
from urllib.request import urlopen
from bs4 import BeautifulSoup

WordScore = namedtuple('WordScore', ['word', 'deg', 'freq', 'score'])
KeywordScore = namedtuple(
    'KeywordScore', ['keyword', 'sum_deg', 'sum_freq', 'score'])

class Rake(object):
    """Extract keywords from a document using the Rapid Automtic Keyword Exraction (RAKE) algorithm.
    Parameters
    ----------
    stop_words_source : string {'fox', 'smart'}, default='fox'
            If 'fox' uses , Fox’s stop word list (Fox 1989). len=425
            If 'smart' uses stop word list from SMART (Salton 1971). len=571
    Attributes
    ----------
    word_scores : list of word scores as namedtuples,
    in descending order of score (deg(w) / freq(w))
            must call `run` first
    keyword_scores : list of keyword scores as namedtuples,
    in descending order of score (sum of word scores)
            must call `run` first

    Implemented from: https://github.com/pmbaumgartner/RAKE/blob/master/rake/rake.py
    """

    def __init__(self, stop_words_source='fox'):
        self.stop_words_source = stop_words_source
        self.phrase_delimiters = [i for i in punctuation]
        self.word_delimiters = [i for i in whitespace]
        self.word_scores = "Call `run` to calculate word scores"
        self.keyword_scores = "Call `run` to calculate keyword scores"

    def _load_stopword_list(self, source='fox'):
        source = source.lower().strip()
        if source == 'smart':
            from .SmartStoplist import stopwords
        elif source == 'fox':
            from .FoxStoplist import stopwords
        else:
            raise ValueError('Stopword source {} not found'.format(source))
        return stopwords

    def _generate_candidate_keywords(self, text, stopwords):
        keywords = []
        phrase_builder = []
        if isinstance(text, list):
            word_array = text
        elif isinstance(text, str):
            word_array = re.split(r'|'.join(self.word_delimiters), text)
        else:
            return "Not tokenized list or text"

        # newlines are split into tokens
        word_array = [word for word in word_array if word]

        for token in word_array:
            word = token.lower()

            # newlines appear as tokens
            # if not token:
            #    continue

            punct_suffix = word[-1] in self.phrase_delimiters
                punct_prefix = word[0] in self.phrase_delimiters
                punct_flag = punct_suffix or punct_prefix
            nonempty_flag = phrase_builder != []

            if punct_suffix:
                word = word[:-1]
                    elif punct_prefix:
                        word = word[1:]

            stopword_flag = word in stopwords

            #print(token, punct_flag, stopword_flag, nonempty_flag)

            if not stopword_flag and not punct_flag:
                phrase_builder.append(word)
            elif stopword_flag and nonempty_flag:
                phrase = ' '.join(phrase_builder)
                keywords.append(phrase)
                phrase_builder = []
            elif punct_flag and nonempty_flag and not stopword_flag:
                phrase_builder.append(word)
                phrase = ' '.join(phrase_builder)
                keywords.append(phrase.strip())
                phrase_builder = []

        return keywords

    def _calculate_word_scores(self, candidate_keywords):
        freq_counter = Counter()
        degree_counter = defaultdict(int)

        for keyword in candidate_keywords:
            word_list = keyword.split()
            degree = len(word_list)
            freq_counter += Counter(word_list)
            for word in word_list:
                degree_counter[word] += degree

        score = {word: round(degree_counter[word] / freq_counter[word], 2) for word in degree_counter.keys()}

        word_scores = []
        for word in score.keys():
            word_tuple = WordScore(word=word,
                                   deg=degree_counter[word],
                                   freq=freq_counter[word],
                                   score=score[word])
            word_scores.append(word_tuple)

        sorted_word_scores = sorted(
            word_scores, key=lambda x: x.score, reverse=True)

        self.word_scores = sorted_word_scores

        return word_scores

    def _calculate_phrase_scores(self, candidate_keywords, word_scores):
        keyword_scores = []

        candidate_keywords = list(set(candidate_keywords))

        for keyword in candidate_keywords:
            word_list = keyword.split()
            words = [
                WordScore for WordScore in word_scores if WordScore.word in word_list]
            keyword_tuple = KeywordScore(keyword=keyword, sum_deg=sum(i.deg for i in words),
                                         sum_freq=sum(i.freq for i in words),
                                         score=sum(i.score for i in words))
            keyword_scores.append(keyword_tuple)

        sorted_keywords = sorted(
            keyword_scores, key=lambda x: x.score, reverse=True)

        return sorted_keywords

    def run(self, text):
        """Runs the RAKE algorithm on `text`
        Parameters
        ----------
        text : string
                A string object containing the text for keyword extraction
        Returns
        -------
        sorted_keywords : list of namedtuples, len=n_keywords
        """
        stopwords = self._load_stopword_list(source=self.stop_words_source)
        candidate_keywords = self._generate_candidate_keywords(text, stopwords)

        word_scores = self._calculate_word_scores(candidate_keywords)
        self.word_scores = word_scores

        keywords = self._calculate_phrase_scores(
            candidate_keywords, word_scores)
        self.keyword_scores = keywords

        return keywords

def extract_keywords(url):
    #extract text from url
    html = urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.body.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    #extract keywords from url text
    rake = Rake()
    keywords = rake.run(text)
    print(keywords)

    #return top 3 keywords
    return keywords[:2]