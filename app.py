import logging
import praw
import json
import os

from config import conservative_subreddits, liberal_subreddits
from analysis import extract_keywords
from database import Database

def get_submissions(reddit):
    submissions = []
    for subreddit_name in conservative_subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        hot_submissions = subreddit.hot(limit=10)
        hot_submissions = [('conservative', x) for x in hot_submissions]
        submissions += hot_submissions

    for subreddit_name in liberal_subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        hot_submissions = subreddit.hot(limit=10)
        hot_submissions = [('liberal', x) for x in hot_submissions]
        submissions += hot_submissions
    
    return submissions

def process_submissions(submissions):
    news_articles = []
    for submission in submissions:
        data = submission[1]
        label = submission[0]

        invalid_content_types = ["jpg", "png", "gif", "jpeg"]
        if any(substring in data.url for substring in invalid_content_types) or data.permalink in data.url:
            continue

        keywords, title = extract_keywords(data.url)

        news_article = {
            "news_type": label,
            "article_url": data.url,
            "upvote_ratio": data.upvote_ratio,
            "title": title,
            "upvotes": data.score,
            "reddit_permalink": data.permalink,
            "keywords": keywords,
            "created_utc": data.created_utc
        }
        print(news_article)
        print('\n\n\n')
        news_articles.append(news_article)

    return news_articles

if __name__ == "__main__":
    logging.info("Running Bifocal News Reddit Scraper")

    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        password=os.environ.get("REDDIT_PASSWORD"),
        username=os.environ.get("REDDIT_USERNAME"),
        user_agent="bifocal_news"
    )

    #get hottest posts from conservative and liberal subreddits
    submissions = get_submissions(reddit)

    #pull necessary information from posts and label
    news_articles = process_submissions(submissions)

    #store headlines in database
    db = Database()
    db.store_news_articles(news_articles)

    for article in news_articles:
        db.store_keywords(article["keywords"])
        db.link_keywords(article["article_url"], article["keywords"])