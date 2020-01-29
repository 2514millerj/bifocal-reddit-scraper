CREATE TABLE NewsArticles (
    title TEXT,
    reddit_permalink TEXT,
    news_type TEXT,
    article_url TEXT PRIMARY KEY,
    upvote_ratio FLOAT,
    upvotes INT,
    created_utc INT
);

CREATE TABLE Keywords (
    keyword TEXT PRIMARY KEY
);

CREATE TABLE ArticleKeywords (
    article_url TEXT,
    keyword TEXT
)