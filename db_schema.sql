DROP TABLE NewsArticles;
DROP TABLE ArticleKeywords;

CREATE TABLE NewsArticles (
    title TEXT,
    reddit_permalink TEXT,
    news_type TEXT,
    article_url TEXT PRIMARY KEY,
    upvote_ratio FLOAT,
    upvotes INT,
    created_utc INT,
    thumbnail_url TEXT
);

CREATE TABLE ArticleKeywords (
    article_url TEXT,
    keyword TEXT,
    created_utc INT,
    PRIMARY KEY (article_url, keyword)
);