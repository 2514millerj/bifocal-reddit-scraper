import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

def store_submissions(a):
    pass

class Database(object):

    def __init__(self):
        self.postgresql_uri = os.environ.get('POSTGRESQL_URI')
        self.engine = create_engine(self.postgresql_uri)
        self.db_conn = self.engine.connect()

    def store_keywords(self, keywords):
        '''
        Input: a list of keywords in the format: [{"keyword": KEYWORD},]
        '''
        statement = text("""INSERT INTO Keywords(keyword) VALUES (:keyword) ON CONFLICT (keyword) DO NOTHING""")
        for keyword in keywords:
            self.db_conn.execute(statement, {"keyword": keyword})

    def store_news_articles(self, article_data):
        statement = text("""INSERT INTO NewsArticles(title, reddit_permalink, article_url, news_type, upvote_ratio, upvotes, created_utc) VALUES (:title, :reddit_permalink, :article_url, :news_type, :upvote_ratio, :upvotes, :created_utc)""")
        
        for article in article_data:
            self.db_conn.execute(statement, **article)

    def link_keywords(self, article_url, keywords):
        statement = text("""INSERT INTO ArticleKeywords(keyword, article_url) VALUES (:keyword, article_url)""")
        for keyword in keywords:
            self.db_conn.execute(statement, {"keyword": keyword, "article_url": article_url})

