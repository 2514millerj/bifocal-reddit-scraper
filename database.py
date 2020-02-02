import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

class Database(object):

    def __init__(self):
        self.postgresql_uri = os.environ.get('POSTGRESQL_URI')
        self.engine = create_engine(self.postgresql_uri)
        self.db_conn = self.engine.connect()

    def store_news_articles(self, article_data):
        statement = text("""INSERT INTO NewsArticles(title, reddit_permalink, article_url, news_type, upvote_ratio, upvotes, created_utc, thumbnail_url) 
                            VALUES (:title, :reddit_permalink, :article_url, :news_type, :upvote_ratio, :upvotes, :created_utc, :thumbnail_url)
                            ON CONFLICT (article_url)
                            DO
                                UPDATE
                                SET upvotes = :upvotes, upvote_ratio = :upvote_ratio""")
        
        for article in article_data:
            self.db_conn.execute(statement, **article)

    def link_keywords(self, article_url, keywords, created_utc):
        statement = text("""INSERT INTO ArticleKeywords(keyword, article_url, created_utc) VALUES (:keyword, :article_url, :created_utc) ON CONFLICT (keyword, article_url) DO NOTHING""")
        for keyword in keywords:
            self.db_conn.execute(statement, {"keyword": keyword, "article_url": article_url, "created_utc": created_utc})

